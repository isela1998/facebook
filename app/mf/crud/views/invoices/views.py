from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from config.settings import MEDIA_URL, STATIC_URL, MEDIA_ROOT
from datetime import date
from os import remove
import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Invoices, DetInvoices, Category, Type_product, CancelledInvoices, Product, CompanySedes, Providers, Facilitator
from mf.crud.forms import InvoicesForm, FacilitatorForm, ProvidersForm, ProductForm, CategoryForm, TypeProductForm
from mf.crud.functions import *

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django_xhtml2pdf.utils import pdf_decorator
from django.contrib.staticfiles import finders

class InvoicesView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'invoices/list.html'
    permission_required = 'view_invoices'
    success_url = reverse_lazy('crud:dashboard')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Invoices.objects.all():
                    item = i.toJSON()
                    data.append(item)
            elif action == 'add-invoice':
                perms = ['add_invoices',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.using(db).get(pk=1)
                    iva = float(1.16)

                    values = json.loads(request.POST['dict'])
                    with transaction.atomic():
                        inv = Invoices()
                        inv.number_invoice = self.get_lastet_invoice()
                        inv.datejoined = request.POST['datejoined']
                        inv.facilitator_id = request.POST['facilitator']
                        inv.provider_id = request.POST['provider']
                        inv.subtotal = float(request.POST['totalInvoice'])
                        inv.expenses = float(request.POST['aditionalExpenses'])
                        inv.total = float(
                            request.POST['totalInvoice']) + float(request.POST['aditionalExpenses'])
                        inv.save()

                        for i in values['products']:
                            price_bs = float(i['final_price']) * float(dolar.dolar)
                            price = price_bs / iva

                            cost = float(i['unit_price']) + float(i['shipment'])
                            gain_margin = float(i['final_price']) - cost

                            product = Product()
                            product.code = i['code']
                            product.product_group_id = 1
                            product.category_id = i['category']
                            product.type_product_id = i['type_product']
                            product.product = i['product']
                            product.cost = cost
                            product.price = price
                            product.price_dl = float(i['final_price'])
                            product.price_bs = price_bs
                            product.gain = gain_margin
                            product.quantity = int(i['quantity'])
                            product.date = request.POST['datejoined']
                            product.save()

                            detInv = DetInvoices()

                            category = Category.objects.get(pk=i['category'])
                            product_type = Type_product.objects.get(
                                pk=i['type_product'])

                            detInv.invoice_id = inv.id
                            detInv.code = i['code']
                            detInv.category = category
                            detInv.type_product = product_type
                            detInv.product = i['product']
                            detInv.total = i['total']
                            detInv.quantity = int(i['quantity'])
                            detInv.unit_price = i['unit_price']
                            detInv.shipment = i['shipment']
                            detInv.gain = i['gain']
                            detInv.final_price = i['final_price']
                            detInv.save()  
            elif action == 'add-provider':
                perms = ['add_providers',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    p = Providers()
                    p.names = request.POST['names']
                    p.identity_id = request.POST['identity']
                    p.ci = request.POST['ci']
                    p.address = request.POST['address']
                    p.contact = request.POST['contact']
                    p.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Agregó un nuevo proveedor')
            elif action == 'add-facilitador':
                perms = ['add_facilitator',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    f = Facilitator()
                    f.names = request.POST['names']
                    f.identity_id = request.POST['identity']
                    f.ci = request.POST['ci']
                    f.contact = request.POST['contact']
                    f.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo facilitador')
            elif action == 'add-category':
                perms = ['add_category',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    ctg = Category()
                    ctg.name = request.POST['name']
                    ctg.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Agregó una nueva Categoría de Producto')
            elif action == 'add-product-type':
                perms = ['add_type_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    type_p = Type_product()
                    type_p.name = request.POST['name']
                    type_p.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró una nuevo tipo de producto')
            elif action == 'get_selects':
                data = []
                category = []
                typeProduct = []

                for i in Category.objects.all():
                    item = i.toJSON()
                    category.append(item)
                for i in Type_product.objects.all():
                    item = i.toJSON()
                    typeProduct.append(item)

                query = {
                    'categories': category,
                    'types': typeProduct
                }
                data.append(query)
            elif action == 'delete':
                perms = ['delete_invoices',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    inv = Invoices.objects.using(db).get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(
                        db, request.user.pk, 'Eliminó el registro de una factura de compra')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_lastet_invoice(self):
        try:
            lastInvoice = Invoices.objects.using(db).last()
            last_invoice = lastInvoice.number_invoice
            new_invoice = int(last_invoice) + 1
        except:
            new_invoice = 1
        n_invoice = f"{new_invoice:0>8}"
        return n_invoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facturas|Compras'
        context['list_url'] = reverse_lazy('crud:invoices')
        context['form'] = InvoicesForm()
        context['formProduct'] = ProductForm()
        context['formCategory'] = CategoryForm()
        context['formProductType'] = TypeProductForm()
        context['formProviders'] = ProvidersForm()
        context['formFacilitator'] = FacilitatorForm()
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

class InvoicesPdfView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    permission_required = 'add_invoices'
    
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    # @pdf_decorator(pdfname='new_filename.pdf')
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('invoices/report.html')
            direction = []

            # http://127.0.0.1:8000/panel/invoices/report/pdf/1/

            db = 'default'
            invoice = Invoices.objects.get(pk=self.kwargs['s'])
            sede = CompanySedes.objects.get(pk=1)

            info = {
                'name': 'IMPORTACIONES SASHA, CA',
                'rif': sede.rif,
                'address': sede.address,
                'postal_zone': sede.postal_zone,
                'phone': sede.phone,
                'email': sede.email,
                'order': invoice.number_invoice,
                'datejoined': invoice.datejoined,
            }

            context = {
                'sale': invoice,
                'comp': info,
                'icon': '{}{}'.format(settings.STATIC_URL, '/img/sasha.png'),
                #'lirax': '{}{}'.format(settings.STATIC_URL, '/img/sasha.png'),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="/Users/Isela/Desktop/'+n_order+'.pdf"'

            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('crud:invoices'))

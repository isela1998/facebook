from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import transaction
import json

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.forms import ProductForm, CategoryForm, TypeProductForm
from mf.crud.models import Product, Category, Type_product, Dolar, CompanySedes
from mf.crud.functions import *

import os
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings
from xhtml2pdf import pisa
from datetime import date

class ProductListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'product/list.html'
    permission_required = 'view_product'

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
                for i in Product.objects.using(db).all().exclude(product_group__id=2):
                    item = i.toJSON()
                    if(i.quantity < 21):
                        css = 'badge badge-danger fill-available text-dark pointer-1'
                    elif(i.quantity > 21):
                        css = 'badge badge-success fill-available text-dark pointer-1'
                    item['css'] = css
                    item['image'] = str(i.image)
                    data.append(item)
            elif action == 'add':
                perms = ['add_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    dolar = Dolar.objects.using(db).get(pk=1)
                    iva = float(1.16)

                    price_dl = float(convertToDecimalFormat(
                        request.POST['price_dl']))
                    cost = float(convertToDecimalFormat(request.POST['cost']))

                    price_bs = price_dl * float(dolar.dolar)
                    price = price_bs / iva

                    gain_margin = price_dl - cost

                    if not request.FILES:
                        image = 'Products/empty.png'
                    else:
                        image = request.FILES['image']
                    product = Product()
                    product.product_group_id = 1
                    product.category_id = request.POST['category']
                    product.type_product_id = request.POST['type_product']
                    product.code = request.POST['code']
                    product.product = request.POST['product']
                    product.quantity = request.POST['quantity']
                    product.cost = cost
                    product.price = price
                    product.price_dl = price_dl
                    product.price_bs = price_bs
                    product.gain = gain_margin
                    product.image = image
                    product.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo producto')
            elif action == 'addCategory':
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
                                    'Registró una nueva categoría de producto')
            elif action == 'addType':
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
            elif action == 'edit':
                perms = ['change_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    if not request.FILES:
                        image = product.image
                    else:
                        image = request.FILES['image']

                    dolar = Dolar.objects.using(db).get(pk=1)
                    iva = float(1.16)

                    if "," not in request.POST['price_dl']:
                        price_dl = float(request.POST['price_dl'])
                    else:
                        price_dl = float(convertToDecimalFormat(
                            request.POST['price_dl']))

                    if "," not in request.POST['cost']:
                        cost = float(request.POST['cost'])
                    else:
                        cost = float(convertToDecimalFormat(request.POST['cost']))

                    price_bs = price_dl * float(dolar.dolar)
                    price = price_bs / iva

                    gain_margin = price_dl - cost

                    product.category = Category.objects.using(
                        db).get(pk=request.POST['category'])
                    product.type_product = Type_product.objects.using(
                        db).get(pk=request.POST['type_product'])
                    product.product = request.POST['product']
                    product.code = request.POST['code']
                    product.quantity = request.POST['quantity']
                    product.cost = cost
                    product.price_dl = price_dl
                    product.price = price
                    product.price_bs = price_bs
                    product.gain = gain_margin
                    product.image = image
                    product.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Editó los datos de un producto')
            elif action == 'down-stock':
                perms = ['change_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    product.product_group_id = 2
                    product.save()
            elif action == 'delete':
                perms = ['delete_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    img = str(product.image)
                    if img == 'Products/empty.png' or img == "":
                        pass
                    else:
                        remove(MEDIA_ROOT + img)
                    product.delete()
                    RegisterOperation(db, request.user.pk,
                                    'Eliminó un producto del almacén')
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos|Stock1'
        context['dl'] = get_dollar()
        context['form'] = ProductForm()
        context['formCategory'] = CategoryForm()
        context['formType'] = TypeProductForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context


class InventaryPdfView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    permission_required = 'add_product'

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

    def get(self, request, *args, **kwargs):
        data = []
        try:
            template = get_template('inventary/report.html')
            direction = []

            warehouse = self.kwargs['i']
            id_bd = self.kwargs['b']
            if id_bd == 1:
                db = 'default'

            today = date.today().strftime('%d-%m-%Y')
            sede = CompanySedes.objects.using('default').get(pk=id_bd)
            direction = {
                'name': 'Multiservicios Fernández, CA',
                'rif': 'J-29441999-2',
                'address': sede.address,
                'postal_zone': sede.postal_zone,
                'phone': sede.phone,
                'email': sede.email,
                'today': today
            }

            if warehouse == 2:
                for i in Product.objects.using(db).all().order_by('category'):
                    data.append(i.toJSON())
            elif warehouse == 1:
                for i in Product_warehouse.objects.using(db).all().order_by('category'):
                    data.append(i.toJSON())

            context = {
                'data': data,
                # 'sale': Sale.objects.using('default').get(pk=self.kwargs['s']),
                'comp': direction,
                'icon': '{}{}'.format(settings.STATIC_URL, '/img/mf.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('crud:almacen_list'))

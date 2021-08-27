from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db import transaction
from datetime import date
import json

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.models import Product, Sale, Budget, DetSale, DetBudget, Client, Method_pay, Debts, Type_debts, Dolar, CompanySedes
from mf.crud.forms import SaleForm, SearchProductForm, ClientForm, MethodPayForm
from mf.crud.functions import *
# from django.db.models import Q

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django_xhtml2pdf.utils import pdf_decorator
from django.contrib.staticfiles import finders

class SaleListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

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
                for i in Sale.objects.using(db).all():
                    item = i.toJSON()
                    if(i.status == 0):
                        css = 'badge badge-success text-dark pointer-1'
                        status = 'Pagada'
                    elif(i.status == 1):
                        css = 'badge badge-warning text-dark pointer-1'
                        status = 'Crédito'
                    elif(i.status == 2):
                        css = 'badge badge-danger text-dark pointer-1'
                        status = 'Anulada'
                    item['statusName'] = status
                    item['css'] = css
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ventas'
        context['create_url'] = reverse_lazy('crud:sale_create')
        context['dl'] = get_dollar()
        context['list_url'] = reverse_lazy('crud:sale_list')
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

class SaleCreateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    permission_required = 'add_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'search_products':
                data = []
                term = request.POST['term']
                code = Product.objects.using(db).filter(code__icontains=term).exclude(quantity__lt=1)[0:10]
                category = Product.objects.using(db).filter(category__name__icontains=term).exclude(quantity__lt=1)[0:10]
                products = Product.objects.using(db).filter(product__icontains=term).exclude(quantity__lt=1)[0:10]
                for i in code:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
                for i in category:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
                for i in products:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                client = Client.objects.using(db).filter(names__icontains=term)[0:10]
                ci = Client.objects.using(db).filter(ci__icontains=term)[0:10]
                for i in client:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + '-' + i.ci
                    data.append(item)
                for b in ci:
                    item = b.toJSON()
                    item['text'] = b.names + ' ' + b.identity.identity + '-' + b.ci
                    data.append(item) 
            elif action == 'add':
                self.addSale(db, request.user.pk, request.POST)
            elif action == 'addBudget':
                datejoined = date.today().strftime('%Y-%m-%d')
                dolar = Dolar.objects.using(db).get(pk=1)
                dl = float(dolar.dolar)

                with transaction.atomic():
                    budget = json.loads(request.POST['sales'])
                    b = Budget()
                    b.datejoined = datejoined
                    b.cli_id = int(request.POST['searchClient'])
                    b.subtotal = float(budget['subtotal'])
                    b.iva = float(budget['iva'])
                    b.total = float(budget['total'])
                    b.total_sale = float(budget['total']) + float(budget['discount'])
                    b.total_sale_dl = (float(budget['total']) + float(budget['discount'])) / float(dl)
                    b.total_dl = float(budget['total']) / float(dl)
                    b.discount = float(budget['discount'])
                    b.discount_dl = float(budget['discount']) / float(dl)
                    b.desc_discount = request.POST['desc_discount']
                    b.type_sale = 'Presupuesto'
                    b.description = request.POST['description']
                    b.budget_number = self.get_lastet_budget()
                    b.rate = float(dl)
                    b.save(using=db)
                    RegisterOperation(db, request.user.pk, 'Generó un nuevo presupuesto')
                    
                    for i in budget['products']:
                        det = DetBudget()
                        pw = Product.objects.get(pk=i['id'])
                        sub = float(pw.price_bs) * float(i['quantity'])
                        sub_dl = float(pw.price_dl) * float(i['quantity'])

                        det.budget_id = b.id
                        det.prod_id = i['id']
                        det.quantity = int(i['quantity'])
                        det.price = float(i['price'])
                        det.price_product_bs = pw.price_bs
                        det.price_product_dl = pw.price_dl
                        det.sub = sub
                        det.subtotal = float(i['subtotal'])
                        det.subtotal_dl = sub_dl
                        det.rate = float(dl)
                        det.save(using=db)
                    data = {
                        'id': b.id,
                    }
            elif action == 'addClient':
                cli = Client()
                cli.names = request.POST['names']
                cli.ci = request.POST['ci']
                cli.address = request.POST['address']
                cli.contact = request.POST['contact']
                cli.save(using='default')
                RegisterOperation(db, request.user.pk, 'Registró un nuevo cliente')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def addSale(self, db, requestUser, requestPOST):
        data = []
        datejoined = date.today().strftime('%Y-%m-%d')
        dolar = Dolar.objects.using(db).get(pk=1)
        dl = float(dolar.dolar)

        clientId = int(requestPOST['searchClient'])

        with transaction.atomic():
            sales = json.loads(requestPOST['sales'])
            sale = Sale()
            sale.datejoined = datejoined
            sale.cli_id = clientId
            sale.subtotal = float(sales['subtotal'])
            sale.iva = float(sales['iva'])
            sale.total = float(sales['total'])
            sale.total_sale = float(sales['total']) + float(sales['discount'])
            sale.total_sale_dl = (float(sales['total']) + float(sales['discount'])) / float(dl)
            sale.total_dl = float(sales['total']) / float(dl)
            sale.discount = float(sales['discount'])
            sale.discount_dl = float(sales['discount']) / float(dl)
            sale.desc_discount = requestPOST['desc_discount']
            type_sale = requestPOST['inlineRadioOptions']
            if type_sale == 'option1':
                sale.type_sale = 'Al Contado'
                sale.method_pay_id = requestPOST['method_pay']
                sale.received = convertToDecimalFormat(requestPOST['received'])
                sale.exchange = convertToDecimalFormat(requestPOST['exchange'])
                sale.method_pay1_id = requestPOST['method_pay1']
                sale.received1 = convertToDecimalFormat(requestPOST['received1'])
                sale.exchange1 = convertToDecimalFormat(requestPOST['exchange1'])
                sale.method_pay2_id = requestPOST['method_pay2']
                sale.received2 = convertToDecimalFormat(requestPOST['received2'])
                sale.exchange2 = convertToDecimalFormat(requestPOST['exchange2'])
            elif type_sale == 'option2':
                sale.type_sale = 'Crédito'
                sale.method_pay_id = 1
                sale.received = '0.00'
                sale.exchange = '0.00'
                sale.method_pay1_id = 1
                sale.received1 = '0.00'
                sale.exchange1 = '0.00'
                sale.method_pay2_id = 1
                sale.received2 = '0.00'
                sale.exchange2 = '0.00'
                sale.status = 1
            sale.rate = float(dl)
            sale.description = requestPOST['description']
            sale.invoice_number = self.get_lastet_invoice(db)
            sale.save(using=db)
            
            RegisterOperation(db, requestUser, 'Registró una nueva venta')      
            
            if(requestPOST['inlineRadioOptions'] == 'option2'):
                d = Debts()
                d.type_debts = Type_debts.objects.using(db).get(pk=1)
                client = Client.objects.using(db).get(pk=clientId)
                d.client = client.names+ ' ' +client.ci+ ' ' +client.address+ ' (' +client.contact+ ')'
                d.description = 'Venta a Crédito'
                d.date = datejoined
                dls = float(sales['total']) / float(dl)
                d.dollars = dls
                d.bs = float(sales['total'])
                d.save(using=db)
                RegisterOperation(db, requestUser, 'Registró una nueva cuenta por cobrar con concepto de Venta a Crédito')

            for i in sales['products']:
                det = DetSale()
                pw = Product.objects.using(db).get(pk=i['id'])
                pw.quantity = int(pw.quantity) - int(i['quantity'])

                sub = float(pw.price_bs) * float(i['quantity'])
                sub_dl = float(pw.price_dl) * float(i['quantity'])
                gain = pw.gain * int(i['quantity'])

                det.sale_id = sale.id
                det.prod_id = i['id']
                det.quantity = int(i['quantity'])
                det.price = pw.price
                det.price_product_bs = pw.price_bs
                det.price_product_dl = pw.price_dl
                det.subtotal = float(pw.price) * float(i['quantity'])
                det.subtotal_dl = sub_dl
                det.sub = sub
                det.gain = gain
                det.rate = float(dl)
                pw.save(using=db)
                det.save(using=db)
            data = {
                'id': sale.id,
                'location': '/panel/sale/add/'
            }
        return data

    def get_methods_pay(self):
        data = []
        for i in Method_pay.objects.all():
            data.append(i.toJSON())
        return data

    def get_lastet_invoice(self, db):
        try:
            lastSale = Sale.objects.using(db).last()
            last_invoice = lastSale.invoice_number
            new_invoice = int(last_invoice) + 1
        except:
            new_invoice = 1
        n_invoice = f"{new_invoice:0>6}"
        return n_invoice

    def get_lastet_budget(self):
        try:
            lastBudget = Budget.objects.last()
            lastNumber = lastBudget.budget_number
            budget = int(lastNumber) + 1
        except:
            budget = 1
        new_budget = f"{budget:0>6}"
        return new_budget

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MÓDULO DE FACTURACIÓN - NUEVA VENTA'
        context['formClient'] = ClientForm()
        context['formMethod'] = MethodPayForm()
        context['methods'] = self.get_methods_pay()
        context['action'] = 'add'
        context['dl'] = get_dollar()
        context['det'] = []
        context['cli'] = []
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

class SaleDuplicateView(LoginRequiredMixin, ValidatePermissionMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    permission_required = 'add_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'search_products':
                data = []
                term = request.POST['term']
                code = Product.objects.using(db).filter(code__icontains=term).exclude(quantity__lt=1)[0:10]
                category = Product.objects.using(db).filter(category__name__icontains=term).exclude(quantity__lt=1)[0:10]
                products = Product.objects.using(db).filter(product__icontains=term).exclude(quantity__lt=1)[0:10]
                for i in code:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
                for i in category:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
                for i in products:
                    item = i.toJSON()
                    item['text'] = '[COD: '+ i.code +'] ' + i.category.name +' - ' + i.product + ' (' + i.type_product.name + ') Precio: ' + item['price_bs'] +'Bs. / '+ item['price_dl'] + '$.'
                    data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                client = Client.objects.using(db).filter(names__icontains=term)[0:10]
                ci = Client.objects.using(db).filter(ci__icontains=term)[0:10]
                for i in client:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + '-' + i.ci
                    data.append(item)
                for b in ci:
                    item = b.toJSON()
                    item['text'] = b.names + ' ' + b.identity.identity + '-' + b.ci
                    data.append(item)
            elif action == 'add':
                self.addSale(db, request.user.pk, request.POST)
            elif action == 'addBudget':
                datejoined = date.today().strftime('%Y-%m-%d')
                dolar = Dolar.objects.using(db).get(pk=1)
                dl = float(dolar.dolar)

                with transaction.atomic():
                    budget = json.loads(request.POST['sales'])
                    b = Budget()
                    b.datejoined = datejoined
                    b.cli_id = int(request.POST['searchClient'])
                    b.subtotal = float(budget['subtotal'])
                    b.iva = float(budget['iva'])
                    b.total = float(budget['total'])
                    b.total_sale = float(budget['total']) + float(budget['discount'])
                    b.total_sale_dl = (float(budget['total']) + float(budget['discount'])) / float(dl)
                    b.total_dl = float(budget['total']) / float(dl)
                    b.discount = float(budget['discount'])
                    b.discount_dl = float(budget['discount']) / float(dl)
                    b.desc_discount = request.POST['desc_discount']
                    b.type_sale = 'Presupuesto'
                    b.description = request.POST['description']
                    b.budget_number = self.get_lastet_budget()
                    b.rate = float(dl)
                    b.save(using=db)
                    RegisterOperation(db, request.user.pk, 'Generó un nuevo presupuesto')

                    for i in budget['products']:
                        det = DetBudget()
                        pw = Product.objects.using(db).get(pk=i['id'])
                        sub = float(pw.price_bs) * float(i['quantity'])
                        sub_dl = float(pw.price_dl) * float(i['quantity'])

                        det.budget_id = b.id
                        det.prod_id = i['id']
                        det.quantity = int(i['quantity'])
                        det.price = float(i['price'])
                        det.price_product_bs = pw.price_bs
                        det.price_product_dl = pw.price_dl
                        det.sub = sub
                        det.subtotal = float(i['subtotal'])
                        det.subtotal_dl = sub_dl
                        det.rate = float(dl)
                        det.save(using=db)
                    data = {
                        'id': b.id,
                    }
            elif action == 'addClient':
                cli = Client()
                cli.names = request.POST['names']
                cli.ci = request.POST['ci']
                cli.address = request.POST['address']
                cli.contact = request.POST['contact']
                cli.save(using='default')
                RegisterOperation(db, request.user.pk, 'Registró un nuevo cliente')
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def addSale(self, db, requestUser, requestPOST):
        data = []
        datejoined = date.today().strftime('%Y-%m-%d')
        dolar = Dolar.objects.using(db).get(pk=1)
        dl = float(dolar.dolar)

        clientId = int(requestPOST['searchClient'])

        with transaction.atomic():
            sales = json.loads(requestPOST['sales'])
            sale = Sale()
            sale.datejoined = datejoined
            sale.cli_id = clientId
            sale.subtotal = float(sales['subtotal'])
            sale.iva = float(sales['iva'])
            sale.total = float(sales['total'])
            sale.total_sale = float(sales['total']) + float(sales['discount'])
            sale.total_sale_dl = (float(sales['total']) + float(sales['discount'])) / float(dl)
            sale.total_dl = float(sales['total']) / float(dl)
            sale.discount = float(sales['discount'])
            sale.discount_dl = float(sales['discount']) / float(dl)
            sale.desc_discount = requestPOST['desc_discount']
            type_sale = requestPOST['inlineRadioOptions']
            if type_sale == 'option1':
                sale.type_sale = 'Al Contado'
                sale.method_pay_id = requestPOST['method_pay']
                sale.received = convertToDecimalFormat(requestPOST['received'])
                sale.exchange = convertToDecimalFormat(requestPOST['exchange'])
                sale.method_pay1_id = requestPOST['method_pay1']
                sale.received1 = convertToDecimalFormat(requestPOST['received1'])
                sale.exchange1 = convertToDecimalFormat(requestPOST['exchange1'])
                sale.method_pay2_id = requestPOST['method_pay2']
                sale.received2 = convertToDecimalFormat(requestPOST['received2'])
                sale.exchange2 = convertToDecimalFormat(requestPOST['exchange2'])
            elif type_sale == 'option2':
                sale.type_sale = 'Crédito'
                sale.method_pay_id = 1
                sale.received = '0.00'
                sale.exchange = '0.00'
                sale.method_pay1_id = 1
                sale.received1 = '0.00'
                sale.exchange1 = '0.00'
                sale.method_pay2_id = 1
                sale.received2 = '0.00'
                sale.exchange2 = '0.00'
                sale.status = 1
            sale.rate = float(dl)
            sale.description = requestPOST['description']
            sale.invoice_number = self.get_lastet_invoice(db)
            sale.save(using=db)
            
            RegisterOperation(db, requestUser, 'Registró una nueva venta')      
            
            if(requestPOST['inlineRadioOptions'] == 'option2'):
                d = Debts()
                d.type_debts = Type_debts.objects.using(db).get(pk=1)
                client = Client.objects.using(db).get(pk=clientId)
                d.client = client.names+ ' ' +client.ci+ ' ' +client.address+ ' (' +client.contact+ ')'
                d.description = 'Venta a Crédito'
                d.date = datejoined
                dls = float(sales['total']) / float(dl)
                d.dollars = dls
                d.bs = float(sales['total'])
                d.save(using=db)
                RegisterOperation(db, requestUser, 'Registró una nueva cuenta por cobrar con concepto de Venta a Crédito')

            for i in sales['products']:
                det = DetSale()
                pw = Product.objects.using(db).get(pk=i['id'])
                pw.quantity = int(pw.quantity) - int(i['quantity'])

                sub = float(pw.price_bs) * float(i['quantity'])
                sub_dl = float(pw.price_dl) * float(i['quantity'])
                gain = pw.gain * int(i['quantity'])

                det.sale_id = sale.id
                det.prod_id = i['id']
                det.quantity = int(i['quantity'])
                det.price = pw.price
                det.price_product_bs = pw.price_bs
                det.price_product_dl = pw.price_dl
                det.subtotal = float(pw.price) * float(i['quantity'])
                det.subtotal_dl = sub_dl
                det.sub = sub
                det.gain = gain
                det.rate = float(dl)
                pw.save(using=db)
                det.save(using=db)
            data = {
                'id': sale.id,
                'location': '/panel/sale/add/'
            }
        return data
        
    def get_methods_pay(self):
        data = []
        for i in Method_pay.objects.all():
            data.append(i.toJSON())
        return data

    def get_lastet_invoice(self, db):
        try:
            lastSale = Sale.objects.last()
            last_invoice = lastSale.invoice_number
            new_invoice = int(last_invoice) + 1
        except:
            new_invoice = 1
        n_invoice = f"{new_invoice:0>6}"
        return n_invoice

    def get_lastet_budget(self):
        try:
            lastBudget = Budget.objects.last()
            lastNumber = lastBudget.budget_number
            budget = int(lastNumber) + 1
        except:
            budget = 1
        new_budget = f"{budget:0>6}"
        return new_budget
 
    def get_pay_details(self):
        try:
            det = Sale.objects.get(pk=self.pk)
            data = {
                'method': det.method_pay.name + ' ' + det.method_pay.type_symbol,
                'quantity': det.received,
                'method2': det.method_pay1.name + ' ' + det.method_pay1.type_symbol,
                'quantity2': det.received1,
                'method3': det.method_pay2.name + ' ' + det.method_pay2.type_symbol,
                'quantity3': det.received2,
                'description': det.description
            }
        except:
            pass
        return data   

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.pk):
                item = i.prod.toJSON()
                item['quantity'] = i.quantity
                data.append(item)
        except:
            pass
        return data

    def get_details_client(self):
        try:
            sale = Sale.objects.get(pk=self.pk)
            c = Client.objects.get(pk=sale.cli_id)
            data = {
                'id': sale.cli_id,
                'names': c.names,
                'ci': c.identity.identity + '-' + c.ci
            }
            
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Módulo de Facturación - Nueva Venta'
        context['entity'] = 'Ventas'
        context['action'] = 'add'
        context['methods'] = self.get_methods_pay()
        context['pays'] = self.get_pay_details()
        context['dl'] = get_dollar()
        context['det'] = json.dumps(self.get_details_product())
        context['cli'] = self.get_details_client()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

class SaleInvoicePdfView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    permission_required = 'add_sale'

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
                    path=result[0]
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
            template = get_template('sale/invoice.html')
            direction = []
            
            db = 'default'

            datejoined = date.today().strftime('%Y-%m-%d')
            sale = Sale.objects.get(pk=self.kwargs['s'])

            sede = CompanySedes.objects.get(pk=1)
            info = {
                'name': 'IMPORTACIONES SASHA, CA',
                'rif': sede.rif,
                'address': sede.address,
                'postal_zone': sede.postal_zone,
                'phone': sede.phone,
                'email': sede.email,
                'order': sale.invoice_number,
                'datejoined': sale.datejoined,
            }

            context = {
                'sale': sale,
                'comp': info,
                'icon': '{}{}'.format(settings.STATIC_URL, '/img/sasha.png'),
                #'lirax': '{}{}'.format(settings.STATIC_URL, '/img/lirax.png'),
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
        return HttpResponseRedirect(reverse_lazy('crud:sale_create'))

class BudgetPdfView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    permission_required = 'add_sale'
    
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
                    path=result[0]
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
            template = get_template('sale/budget.html')
            direction = []

            db = 'default'

            budget = Budget.objects.using(db).get(pk=self.kwargs['s'])
            sede = CompanySedes.objects.using('default').get(pk=1)
            direction = {
                'name': 'IMPORTACIONES SASHA, CA',
                'rif': sede.rif,
                'address': sede.address,
                'postal_zone': sede.postal_zone,
                'phone': sede.phone,
                'email': sede.email,
                'order': budget.budget_number,
                'datejoined': budget.datejoined,
                'date_end': budget.datejoined,
            }

            context = {
                'sale': budget,
                'comp': direction,
                'icon': '{}{}'.format(settings.STATIC_URL, '/img/sasha.png'),
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
        return HttpResponseRedirect(reverse_lazy('crud:sale_create')) 

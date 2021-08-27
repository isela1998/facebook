from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db import transaction
from datetime import date
import json

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.models import Product, Sale, DetSale, Client,  Method_pay, Debts, Type_debts, Dolar, Method_pay
from mf.crud.forms import SaleForm, SearchProductForm, ClientForm, MethodPayForm
from mf.crud.functions import *
# from django.db.models import Q

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class SalesSummaryListView(LoginRequiredMixin, ValidatePermissionMixin, ListView):
    model = Sale
    template_name = 'salesSummary/list.html'
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
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_type_sales(day_querie)
            elif action == 'searchdata2':
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_pay_method(day_querie)
            elif action == 'searchdata3':
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_sales_discount(day_querie)
            elif action == 'searchdata5':
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_sales_return(day_querie)
            elif action == 'searchdata6':
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_gains_details(day_querie)
            elif action == 'search_totals':
                day = request.POST['day']
                day_querie = self.getDay(day)
                data = self.get_totals_details(day_querie)
            elif action == 'search_details':
                day = request.POST['day']
                day_querie = self.getDay(day)
                params = request.POST['params']
                search = request.POST['search']
                data = self.search_details(search, params, day_querie)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def getDay(self, day):
        if(day == 'null'):
            day_querie = date.today().strftime('%Y-%m-%d')
        else:
            day_querie = day
        return day_querie

    def get_type_sales(self, day_querie):
        data = []
        day_today = day_querie
        try:
            type_sale1 = 'Al Contado'
            type_sale2 = 'Crédito'

            quantity_type1 = 0
            for i in Sale.objects.filter(type_sale=type_sale1, datejoined=day_today).exclude(status=2):
                quantity_type1 = int(quantity_type1) + 1

            quantity_type2 = 0
            for i in Sale.objects.filter(type_sale=type_sale2, datejoined=day_today).exclude(status=2):
                quantity_type2 = int(quantity_type2) + 1

            infoSale1 = {
                'type_sale': type_sale1,
                'quantity': quantity_type1,
            }
            infoSale2 = {
                'type_sale': type_sale2,
                'quantity': quantity_type2,
            }
            data.append(infoSale1)
            data.append(infoSale2)
        except:
            pass
        return data

    def get_gains_details(self, day_querie):
        data = []

        idProduct = 0
        products = Product.objects.all()
        detSales = DetSale.objects.filter(
            sale__datejoined=day_querie).exclude(sale__status=2)

        for p in products:
            idProduct = p.id
            nameProduct = p.product + ' (' + p.type_product.name + ')',
            quantity = 0
            total = 0
            gain = 0
            for i in detSales:
                if i.prod.id == idProduct:
                    quantity = quantity + i.quantity
                    total = total + i.subtotal_dl
                    gain = gain + i.gain
            if quantity > 0:
                details = {
                    'product': nameProduct,
                    'quantity': quantity,
                    'total': total,
                    'gain': gain
                }
                data.append(details)
        return data

    def get_totals_details(self, day_querie):
        data = []
        totalsDl = 0
        totalsGains = 0
        quantity = 0

        detSales = DetSale.objects.filter(
            sale__datejoined=day_querie).exclude(sale__status=2)
        for i in detSales:
            totalsDl = totalsDl + i.subtotal_dl
            totalsGains = totalsGains + i.gain
            quantity = quantity + i.quantity
        details = {
            'quantity': quantity,
            'totalDl': totalsDl,
            'totalGains': totalsGains,
        }
        data.append(details)
        return data

    def get_pay_method(self, day_querie):
        data = []
        day_today = day_querie
        try:
            for i in Method_pay.objects.all().exclude(pk=1):
                pk = i.id
                name = i.name
                quantity = 0
                total = 0
                type_total = i.type_symbol
                for s in Sale.objects.filter(datejoined=day_today).exclude(status=2):
                    if s.method_pay.id == pk:
                        json = s.toJSON()
                        quantity = int(quantity) + 1
                        total = total + (float(s.received) - float(s.exchange))
                    elif s.method_pay1.id == pk:
                        json = s.toJSON()
                        quantity = int(quantity) + 1
                        total = total + (float(s.received1) -
                                         float(s.exchange1))
                    elif s.method_pay2.id == pk:
                        json = s.toJSON()
                        quantity = int(quantity) + 1
                        total = total + (float(s.received2) -
                                         float(s.exchange2))
                result = {
                    'id': pk,
                    'method': name,
                    'quantity': quantity,
                    'total': total,
                    'type_total': type_total,
                }
                data.append(result)
        except:
            pass
        return data

    def get_sales_discount(self, day_querie):
        data = []
        day_today = day_querie
        try:
            quantity = 0
            for i in Sale.objects.filter(datejoined=day_today).exclude(desc_discount__endswith='APLICA').exclude(status=2):
                quantity = quantity + 1
            info = {
                'name': 'Ventas',
                'quantity': quantity,
            }
            data.append(info)
        except:
            pass
        return data

    def search_details(self, search, params, day_querie):
        data = []
        day_today = day_querie
        try:
            if search == 'TypeSales':
                for i in Sale.objects.filter(type_sale=params, datejoined=day_today).exclude(status=2):
                    json = i.toJSON()
                    sale = self.createDictDetails(i, json)
                    data.append(sale)
            elif search == 'PayMethod':
                for i in Sale.objects.filter(datejoined=day_today).exclude(status=2):
                    if i.method_pay.id == int(params):
                        json = i.toJSON()
                        sale = self.createDictDetails(i, json)
                        data.append(sale)
                    elif i.method_pay1.id == int(params):
                        json = i.toJSON()
                        sale = self.createDictDetails(i, json)
                        data.append(sale)
                    elif i.method_pay2.id == int(params):
                        json = i.toJSON()
                        sale = self.createDictDetails(i, json)
                        data.append(sale)
            elif search == 'SDiscount':
                for i in Sale.objects.filter(datejoined=day_today).exclude(desc_discount__endswith='aplica').exclude(status=2):
                    json = i.toJSON()
                    sale = self.createDictDetails(i, json)
                    data.append(sale)
        except:
            pass
        return data

    def createDictDetails(self, i, json):
        if(i.status == 0):
            status = 'Pagada'
        elif(i.status == 1):
            status = 'Emitida'
        sale = {
            'date': i.datejoined,
            'invoice_number': i.invoice_number,
            'status': status,
            'client': i.cli.names + ' (' + i.cli.ci + ') ',
            'method': i.method_pay.name,
            'abrev_method': i.method_pay.type_symbol,
            'method1': i.method_pay1.name,
            'abrev_method1': i.method_pay1.type_symbol,
            'method2': i.method_pay2.name,
            'abrev_method2': i.method_pay2.type_symbol,
            'discount': i.discount,
            'desc_discount': i.desc_discount,
            'received': i.received,
            'exchange': i.exchange,
            'received1': i.received1,
            'exchange1': i.exchange1,
            'received2': i.received2,
            'exchange2': i.exchange2,
            'description': i.description,
            'total': float(i.total),
            'total_dl': float(i.total_dl),
            'det': json['det']
        }
        return sale

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resumen|Ventas'
        context['dl'] = get_dollar()
        context['list_url'] = reverse_lazy('crud:summary_list')
        context['today'] = date.today().strftime('%Y-%m-%d')
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

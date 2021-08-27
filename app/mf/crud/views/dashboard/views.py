from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from urllib import request
from django.utils import timezone
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from mf.crud.models import Sale, DetSale, Product, Dolar, Requested, Permisology, Debts, DollarHistory

from datetime import date
from datetime import datetime, timedelta

from django.db.models.functions import Coalesce
from django.db.models import Sum

from mf.crud.functions import *

class DashboardView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'dashboard.html'
    permission_required = 'view_client'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'get_sales_today':
                data = []
                sales = self.get_sales_today(db)
                data.append(sales)
            elif action == 'get_few_products':
                data = []
                products = self.get_few_products(db)
                data.append(products)
            elif action == 'upDolar':
                perms = ['change_dolar', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    with transaction.atomic():
                        generalRate = float(
                            convertToDecimalFormat(request.POST['dolar']))
                        try:
                            dolar = Dolar.objects.get(pk=1)
                            dolar.dolar = generalRate
                            dolar.save(using='default')
                        except:
                            dolar = Dolar()
                            dolar.dolar = generalRate
                            dolar.save(using='default')

                        RegisterOperation(db, request.user.pk,
                                        'Actualizó las Tasas del Dolar')

                        history = DollarHistory()
                        date = timezone.localtime(timezone.now())
                        history.datejoined = date.strftime(
                            '%Y-%m-%d | %H:%M:%S %p')
                        history.rate_dolar1 = generalRate
                        history.save(using='default')

                        self.update_prices(generalRate)
            elif action == 'get_graph_sales':
                year = datetime.now().year
                for m in range(1, 13):
                    total = Sale.objects.using(db).filter(datejoined__year=year, datejoined__month=m).aggregate(
                        r=Coalesce(Sum('total'), 0)).get('r')
                data = {
                    'name': 'Porcentaje de ventas',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales(db)
                }
            elif action == 'get_graph_products':
                data = {
                    'name': 'Ventas',
                    'text': 'Productos',
                    'colorByPoint': True,
                    'data': self.get_graph_products(db)
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_sales_today(self, db):
        data = 0
        try:
            day = datetime.now().day
            sales = Sale.objects.using(db).filter(datejoined__day=day)
            total = 0
            for i in sales:
                total = int(total) + 1
                data = total
        except:
            pass
        return data

    def get_few_products(self, db):
        data = 0
        try:
            products = Product.objects.using(db).filter(quantity__lt=5)
            total = 0
            for i in products:
                total = int(total) + 1
                data = total
        except:
            pass
        return data

    def update_prices(self, dl):
        iva = 1.16
        # Price update to DB Products
        product = Product.objects.all()
        if not product:
            pass
        else:
            for p in product:
                p.price_bs = float(p.price_dl) * dl
                p.price = (float(p.price_dl) * dl) / iva
                p.save()

        # Price update to DB Product_warehouse
        product_v = Product.objects.all()
        if not product_v:
            pass
        else:
            for p in product_v:
                p.price_bs = float(p.price_dl) * dl
                p.price = (float(p.price_dl) * dl) / iva
                p.save()

        # Price update to DB Debts
        debts = Debts.objects.all()
        if not debts:
            pass
        else:
            for d in debts:
                d.bs = float(d.dollars) * dl
                d.save()

    def get_graph_sales(self, db):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.using(db).filter(datejoined__year=year, datejoined__month=m).aggregate(
                    r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_products(self, db):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.using(db).all():
                total = DetSale.objects.using(db).filter(sale__datejoined__year=year, sale__datejoined__month=month, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.brand + ' ' + p.product + ' ' + '(' + p.type_product.name + ')',
                        'y': float(total)
                    })
        except:
            pass
        return data

    def get_name_month(self):
        data = ''
        month = datetime.now().month
        if month == 1:
            data = 'Enero'
        elif month == 2:
            data = 'Febrero'
        elif month == 3:
            data = 'Marzo'
        elif month == 4:
            data = 'Abril'
        elif month == 5:
            data = 'Mayo'
        elif month == 6:
            data = 'Junio'
        elif month == 7:
            data = 'Julio'
        elif month == 8:
            data = 'Agosto'
        elif month == 9:
            data = 'Septiembre'
        elif month == 10:
            data = 'Octubre'
        elif month == 11:
            data = 'Noviembre'
        elif month == 12:
            data = 'Diciembre'
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'PRINCIPAL'
        context['dl'] = get_dollar()
        context['today'] = date.today()
        context['month'] = self.get_name_month()
        context['year'] = datetime.now().year
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today()
        context['title_pag'] = ''
        return context

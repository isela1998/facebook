from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Earnings, Dolar
from mf.crud.forms import EarningsForm
from mf.crud.functions import *

class EarningsListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'earnings/list.html'
    permission_required = 'view_earnings'

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
                for i in Earnings.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_earnings',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.using(db).get(pk=1)
                    dl = float(dolar.dolar)
                    p = float(convertToDecimalFormat(request.POST['amount_dl']))

                    iva = 1.16
                    bs = p * dl

                    e = Earnings()
                    e.date = request.POST['date']
                    e.concept = request.POST['concept']
                    e.amount_dl = p
                    e.amount_bs = bs
                    e.save(using=db)
                    RegisterOperation(db, request.user.pk, 'Registró datos de nueva ganancia')
            elif action == 'edit':
                perms = ['change_earnings',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.using(db).get(pk=1)
                    dl = float(dolar.dolar)

                    if not ',' in request.POST['amount_dl']:
                        p = float(request.POST['amount_dl'])
                    else:
                        p = float(convertToDecimalFormat(request.POST['amount_dl']))

                    iva = 1.16
                    bs = p * dl

                    e = Earnings.objects.using(db).get(pk=request.POST['id'])
                    e.date = request.POST['date']
                    e.concept = request.POST['concept']
                    e.amount_dl = p
                    e.amount_bs = bs
                    e.save(using=db)
                    RegisterOperation(db, request.user.pk, 'Editó los datos de una ganancia')
            elif action == 'delete':
                perms = ['delete_earnings',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Earnings.objects.using(db).get(pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk, 'Eliminó el registro de una ganancia')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ganancias'
        context['list_url'] = reverse_lazy('crud:earnings_list')
        context['dl'] = get_dollar()
        context['form'] = EarningsForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from mf.crud.forms import ExpensesForm
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from mf.crud.models import Expenses, Dolar
from mf.crud.functions import *

class ExpensesListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'expenses/list.html'
    permission_required = 'view_expenses'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Expenses.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_expenses',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.get(pk=1)
                    dl = float(dolar.dolar)

                    p = float(convertToDecimalFormat(request.POST['amount_dl']))
                    bs = p * dl

                    e = Expenses()
                    e.date = request.POST['date']
                    e.concept = request.POST['concept']
                    e.amount_dl = p
                    e.amount_bs = bs
                    e.save()
            elif action == 'edit':
                perms = ['change_expenses',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.get(pk=1)
                    dl = float(dolar.dolar)

                    if not ',' in request.POST['amount_dl']:
                        p = float(request.POST['amount_dl'])
                    else:
                        p = float(convertToDecimalFormat(request.POST['amount_dl']))

                    bs = p * dl

                    e = Expenses.objects.get(pk=request.POST['id'])
                    e.date = request.POST['date']
                    e.concept = request.POST['concept']
                    e.amount_dl = p
                    e.amount_bs = bs
                    e.save()
            elif action == 'delete':
                perms = ['delete_expenses',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Expenses.objects.get(pk=request.POST['id']).delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gastos'
        context['list_url'] = reverse_lazy('crud:expenses_list')
        context['dl'] = get_dollar()
        context['form'] = ExpensesForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

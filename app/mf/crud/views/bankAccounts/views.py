from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from config.settings import MEDIA_URL, STATIC_URL, MEDIA_ROOT
from os import remove

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import BankAccounts
from mf.crud.forms import BankAccountsForm
from mf.crud.functions import *


class BankAccountsView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'bankAccounts/list.html'
    permission_required = 'view_bankaccounts'

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
                for i in BankAccounts.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_bankaccounts', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    b = BankAccounts()
                    b.bank = request.POST['bank']
                    b.accountHolder = request.POST['accountHolder']
                    b.holderId = request.POST['holderId']
                    b.accountNumber = request.POST['accountNumber']
                    b.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                      'Agregó una cuenta bancaria')
            elif action == 'edit':
                perms = ['change_bankaccounts', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    b = BankAccounts.objects.using(
                        db).get(pk=request.POST['id'])
                    b.bank = request.POST['bank']
                    b.accountHolder = request.POST['accountHolder']
                    b.holderId = request.POST['holderId']
                    b.accountNumber = request.POST['accountNumber']
                    b.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                      'Editó los datos de una cuenta bancaria.')
            elif action == 'delete':
                perms = ['delete_bankaccounts', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    BankAccounts.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                      'Eliminó una cuenta bancaria..')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cuentas Bancarias'
        context['list_url'] = reverse_lazy('crud:bankAccounts')
        context['form'] = BankAccountsForm()
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today()
        return context

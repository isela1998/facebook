from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Method_pay
from mf.crud.forms import MethodPayForm
from mf.crud.functions import *


class MethodListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'method/list.html'
    permission_required = 'view_method_pay'

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
                for i in Method_pay.objects.using(db).all().exclude(pk=1):
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_method_pay',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    method = Method_pay()
                    method.name = request.POST['name']
                    method.type_symbol = request.POST['type_symbol']
                    method.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo Método de Pago')
            elif action == 'edit':
                perms = ['change_method_pay',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    method = Method_pay.objects.using(
                        db).get(pk=request.POST['id'])
                    method.name = request.POST['name']
                    method.type_symbol = request.POST['type_symbol']
                    method.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Editó un nuevo Método de Pago')
            elif action == 'delete':
                perms = ['delete_method_pay',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Method_pay.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                    'Borró un Método de Pago')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Métodos de Pago'
        context['list_url'] = reverse_lazy('crud:method_list')
        context['dl'] = get_dollar()
        context['form'] = MethodPayForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

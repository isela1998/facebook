from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.models import Providers
from mf.crud.forms import ProvidersForm
from mf.crud.functions import *

class ProvidersView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'providers/list.html'
    permission_required = 'view_providers'

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
                for i in Providers.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
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
                                    'Registró un nuevo proveedor')
            elif action == 'edit':
                perms = ['change_providers',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    p = Providers.objects.using(db).get(pk=request.POST['id'])
                    p.names = request.POST['names']
                    p.identity_id = request.POST['identity']
                    p.ci = request.POST['ci']
                    p.address = request.POST['address']
                    p.contact = request.POST['contact']
                    p.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Editó los datos de un proveedor')
            elif action == 'delete':
                perms = ['delete_providers',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Providers.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                    'Eliminó el registro de un proveedor')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proveedores'
        context['list_url'] = reverse_lazy('crud:providers')
        context['dl'] = get_dollar()
        context['form'] = ProvidersForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

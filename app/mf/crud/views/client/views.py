from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Client
from mf.crud.forms import ClientForm
from mf.crud.functions import *

class ClientView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'client/list.html'
    permission_required = 'view_client'

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
                for i in Client.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_client',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    cli = Client()
                    cli.names = request.POST['names']
                    cli.identity_id = request.POST['identity']
                    cli.ci = request.POST['ci']
                    cli.address = request.POST['address']
                    cli.contact = request.POST['contact']
                    cli.save(using='default')
                    RegisterOperation(db, request.user.pk, 'Registró un nuevo cliente')
            elif action == 'edit':
                perms = ['change_client',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    cli = Client.objects.using(db).get(pk=request.POST['id'])
                    cli.names = request.POST['names']
                    cli.identity_id = request.POST['identity']
                    cli.ci = request.POST['ci']
                    cli.address = request.POST['address']
                    cli.contact = request.POST['contact']
                    cli.save(using='default')
                    RegisterOperation(db, request.user.pk, 'Editó la información personal de un cliente')
            elif action == 'delete':
                perms = ['delete_client',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Client.objects.using('default').get(pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk, 'Eliminó un cliente')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['list_url'] = reverse_lazy('crud:client')
        context['dl'] = get_dollar()
        context['form'] = ClientForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

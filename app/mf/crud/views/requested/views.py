from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.models import Requested
from mf.crud.forms import RequestedForm
from mf.crud.functions import *


class RequestedView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'requested/list.html'
    permission_required = 'view_requested'

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
                for i in Requested.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_requested',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    r = Requested()
                    r.name = request.POST['name']
                    r.description = request.POST['description']
                    r.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo producto solicitado')
            elif action == 'edit':
                perms = ['change_requested']
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    r = Requested.objects.using(db).get(pk=request.POST['id'])
                    r.name = request.POST['name']
                    r.description = request.POST['description']
                    r.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                      'Editó los datos de producto solicitado')
            elif action == 'delete':
                perms = ['delete_requested']
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Requested.objects.using(db).get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(
                        db, request.user.pk, 'Eliminó el registro de un producto solicitado')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('crud:requested_list')
        context['title'] = 'Solicitados'
        context['entity'] = 'Productos'
        context['dl'] = get_dollar()
        context['form'] = RequestedForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

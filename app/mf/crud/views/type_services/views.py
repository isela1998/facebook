from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.forms import TypeServicesForm
from mf.crud.models import Type_services
from mf.crud.functions import *

class TypeServicesListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'typeServices/list.html'
    permission_required = 'view_type_services'

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
                for i in Type_services.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_type_services', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    services = Type_services()
                    services.name = request.POST['name']
                    services.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                      'Registró una nuevo tipo de servicio')
            elif action == 'edit':
                perms = ['change_type_services', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    services = Type_services.objects.using(
                        db).get(pk=request.POST['id'])
                    services.name = request.POST['name']
                    services.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                      'Editó un tipo de servicio')
            elif action == 'delete':
                perms = ['delete_type_services', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Type_services.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                      'Eliminó un tipo de servicio')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Servicios'
        context['list_url'] = reverse_lazy('crud:type_services_list')
        context['dl'] = get_dollar()
        context['form'] = TypeServicesForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

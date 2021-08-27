from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Facilitator
from mf.crud.forms import FacilitatorForm
from mf.crud.functions import *


class FacilitatorView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'facilitator/list.html'
    permission_required = 'view_facilitator'

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
                for i in Facilitator.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_facilitator', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    f = Facilitator()
                    f.names = request.POST['names']
                    f.identity_id = request.POST['identity']
                    f.ci = request.POST['ci']
                    f.contact = request.POST['contact']
                    f.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                      'Registró un nuevo facilitador')
            elif action == 'edit':
                perms = ['change_facilitator', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    f = Facilitator.objects.using(
                        db).get(pk=request.POST['id'])
                    f.names = request.POST['names']
                    f.identity_id = request.POST['identity']
                    f.ci = request.POST['ci']
                    f.contact = request.POST['contact']
                    f.save(using='default')
                    RegisterOperation(
                        db, request.user.pk, 'Editó la información personal de un facilitador')
            elif action == 'delete':
                perms = ['delete_facilitator', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Facilitator.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                      'Eliminó un facilitador')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facilitadores'
        context['list_url'] = reverse_lazy('crud:facilitator')
        context['dl'] = get_dollar()
        context['form'] = FacilitatorForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

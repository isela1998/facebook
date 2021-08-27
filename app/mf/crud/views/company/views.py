from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.forms import CompanySedesForm
from mf.crud.models import CompanyInfo, CompanySedes
from mf.crud.functions import *

class CompanyListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'company/list.html'
    permission_required = 'view_companysedes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        bd = 'default'
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CompanySedes.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'edit':
                perms = ['change_companysedes',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    c = CompanySedes.objects.using(db).get(pk=request.POST['id'])
                    c.rif = request.POST['rif']
                    c.address = request.POST['address']
                    c.postal_zone = request.POST['postal_zone']
                    c.phone = request.POST['phone']
                    c.email = request.POST['email']
                    c.save(using='default')
                    RegisterOperation(db, request.user.pk, 'Editó la información de una sede')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'IMPORTACIONES SASHA, CA'
        context['list_url'] = reverse_lazy('crud:company_list')
        context['dl'] = get_dollar()
        context['form'] = CompanySedesForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

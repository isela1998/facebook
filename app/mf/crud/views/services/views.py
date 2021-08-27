from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from mf.crud.forms import ServicesForm
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from mf.crud.models import Services, Dolar
from mf.crud.functions import *

class ServicesListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'services/list.html'
    permission_required = 'view_services'

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
                for i in Services.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_services',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.get(pk=1)
                    dl = float(dolar.dolar)

                    if not ',' in request.POST['amount_dl']:
                        amount_dl = float(request.POST['amount_dl'])
                    else:
                        amount_dl = float(convertToDecimalFormat(request.POST['amount_dl']))

                    amount_bs = amount_dl * dl

                    s = Services()
                    s.datejoined = request.POST['datejoined']
                    s.type_service_id = request.POST['type_service']
                    s.quantity = request.POST['quantity']
                    s.amount_dl = amount_dl
                    s.amount_bs = amount_bs
                    s.description = request.POST['description']
                    s.save()
            elif action == 'edit':
                perms = ['change_services',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.get(pk=1)
                    dl = float(dolar.dolar)

                    if not ',' in request.POST['amount_dl']:
                        amount_dl = float(request.POST['amount_dl'])
                    else:
                        amount_dl = float(convertToDecimalFormat(request.POST['amount_dl']))

                    amount_bs = amount_dl * dl

                    s = Services.objects.get(pk=request.POST['id'])
                    s.datejoined = request.POST['datejoined']
                    s.type_service_id = request.POST['type_service']
                    s.quantity = request.POST['quantity']
                    s.amount_dl = amount_dl
                    s.amount_bs = amount_bs
                    s.description = request.POST['description']
                    s.save()
            elif action == 'delete':
                perms = ['delete_services',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Services.objects.get(pk=request.POST['id']).delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Servicios'
        context['list_url'] = reverse_lazy('crud:services_list')
        context['dl'] = get_dollar()
        context['form'] = ServicesForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

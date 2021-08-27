from config.settings import MEDIA_URL, STATIC_URL, MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from os import remove

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Payments
from mf.crud.forms import PaymentsForm
from mf.crud.functions import *

class PaymentsView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'payments/list.html'
    permission_required = 'view_payments'
    success_url = reverse_lazy('crud:dashboard')

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
                for i in Payments.objects.using(db).all():
                    item = i.toJSON()
                    item['image'] = str(i.image)
                    data.append(item)
            elif action == 'edit':
                perms = ['change_payments',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    p = Payments.objects.using(db).get(pk=request.POST['id'])
                    if not request.FILES:
                        image = p.image
                    else:
                        image = request.FILES['image']
                    if not ',' in request.POST['quantity']:
                        q = float(request.POST['quantity'])
                    else:
                        q = float(convertToDecimalFormat(request.POST['quantity']))

                    p.pay_date = request.POST['pay_date']
                    p.provider = request.POST['provider']
                    p.description = request.POST['description']
                    p.quantity = q
                    p.image = image
                    p.save(using=db)
                    RegisterOperation(
                        db, request.user.pk, 'Editó los datos de un registro de abono de factura')
            elif action == 'delete':
                perms = ['delete_payments',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    p = Payments.objects.using(db).get(pk=request.POST['id'])
                    img = str(p.image)
                    if img == 'Cap_Payments/empty.png':
                        pass
                    else:
                        remove(MEDIA_ROOT + img)
                    p.delete()
                    RegisterOperation(db, request.user.pk,
                                    'Eliminó el registro de un Abono de Factura')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Abonos|Facturas'
        context['list_url'] = reverse_lazy('crud:payments')
        context['form'] = PaymentsForm()
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

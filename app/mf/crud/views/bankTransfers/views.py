from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from config.settings import MEDIA_URL, STATIC_URL, MEDIA_ROOT
from os import remove

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import BankTransfers
from mf.crud.forms import BankTransfersForm
from mf.crud.functions import *

class BankTransfersView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'bankTransfers/list.html'
    permission_required = 'view_banktransfers'

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
                for i in BankTransfers.objects.using(db).all():
                    item = i.toJSON()
                    item['image'] = str(i.image)
                    data.append(item)
            elif action == 'add':
                perms = ['add_banktransfers', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    if not request.FILES:
                        image = 'Cap_Banktransfers/empty.png'
                    else:
                        image = request.FILES['image']
                    total = convertToDecimalFormat(request.POST['total'])
                    b = BankTransfers()
                    b.pay_date = request.POST['pay_date']
                    b.referenceNumber = request.POST['referenceNumber']
                    b.bank_id = request.POST['bank']
                    b.total = total
                    b.description = request.POST['description']
                    b.image = image
                    b.save(using=db)
                    RegisterOperation(
                        db, request.user.pk, 'Registró los datos de una transferencia bancaria recibida')
            elif action == 'edit':
                perms = ['change_banktransfers', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    b = BankTransfers.objects.using(
                        db).get(pk=request.POST['id'])
                    image = ''
                    if not request.FILES:
                        image = b.image
                    else:
                        image = request.FILES['image']

                    if "," not in request.POST['total']:
                        total = request.POST['total']
                    else:
                        total = convertToDecimalFormat(request.POST['total'])
                    b.pay_date = request.POST['pay_date']
                    b.referenceNumber = request.POST['referenceNumber']
                    b.bank_id = request.POST['bank']
                    b.total = total
                    b.description = request.POST['description']
                    b.image = image
                    b.save(using=db)
                    RegisterOperation(
                        db, request.user.pk, 'Editó los datos de una transferencia bancaria recibida')
            elif action == 'delete':
                perms = ['delete_banktransfers', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    b = BankTransfers.objects.using(
                        db).get(pk=request.POST['id'])
                    img = str(b.image)
                    if img == 'Cap_Banktransfers/empty.png':
                        pass
                    else:
                        remove(MEDIA_ROOT + img)
                    b.delete()
                    RegisterOperation(
                        db, request.user.pk, 'Borró el registro de una transferencia bancaria recibida')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Transferencias Bancarias'
        context['list_url'] = reverse_lazy('crud:bankTransfers')
        context['form'] = BankTransfersForm()
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today()
        return context

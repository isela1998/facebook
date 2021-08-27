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

from mf.crud.models import CancelledInvoices, Providers
from mf.crud.forms import CancelledInvoicesForm, ProvidersForm
from mf.crud.functions import *


class CancelledInvoicesView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'cancelledInvoices/list.html'
    permission_required = 'view_cancelledinvoices', 'add_cancelledinvoices', 'change_cancelledinvoices', 'delete_cancelledinvoices'
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
                for i in CancelledInvoices.objects.using(db).all():
                    item = i.toJSON()
                    data.append(item)
            elif action == 'add':
                image = ''
                if not request.FILES:
                    image = 'Cap_Facturas/empty.png'
                else:
                    image = request.FILES['image']
                c = CancelledInvoices()
                c.pay_date = request.POST['pay_date']
                c.provider_id = request.POST['provider']
                c.description = request.POST['description']
                c.quantity = float(convertToDecimalFormat(
                    request.POST['quantity']))
                c.image = image
                c.save(using=db)
                RegisterOperation(db, request.user.pk,
                                  'Registró los datos de una factura cancelada')
            elif action == 'addProvider':
                p = Providers()
                p.names = request.POST['names']
                p.identity_id = request.POST['identity']
                p.ci = request.POST['ci']
                p.address = request.POST['address']
                p.contact = request.POST['contact']
                p.save(using='default')
                RegisterOperation(db, request.user.pk,
                                  'Agregó un nuevo proveedor')
            elif action == 'edit':
                image = ''
                c = CancelledInvoices.objects.using(
                    db).get(pk=request.POST['id'])
                if not request.FILES:
                    image = c.image
                else:
                    image = request.FILES['image']

                if not ',' in request.POST['quantity']:
                    q = float(request.POST['quantity'])
                else:
                    q = float(convertToDecimalFormat(request.POST['quantity']))

                c.pay_date = request.POST['pay_date']
                c.provider_id = request.POST['provider']
                c.description = request.POST['description']
                c.quantity = q
                c.image = image
                c.save(using=db)
                RegisterOperation(db, request.user.pk,
                                  'Editó los datos de una factura cancelada')
            elif action == 'delete':
                c = CancelledInvoices.objects.using(
                    db).get(pk=request.POST['id'])
                img = str(c.image)
                if img == 'Cap_Facturas/empty.png':
                    pass
                else:
                    remove(MEDIA_ROOT + img)
                c.delete()
                RegisterOperation(
                    db, request.user.pk, 'Eliminó el registro de una factura cancelada')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pagos de Facturas'
        context['list_url'] = reverse_lazy('crud:cancelledInvoices')
        context['form'] = CancelledInvoicesForm()
        context['formProviders'] = ProvidersForm()
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

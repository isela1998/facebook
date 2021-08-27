from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.forms import DebtsForm, ClientForm, ProvidersForm, PaymentsForm, CancelledInvoicesForm
from mf.crud.models import Debts, Type_debts, Dolar, Permisology, Client, Providers, Payments, CancelledInvoices, Client
from mf.crud.functions import *


class DebtsListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'debts/list.html'
    permission_required = 'view_debts'

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
                for i in Debts.objects.using(db).all():
                    item = i.toJSON()
                    if(i.type_debts.name == 'Cobrar'):
                        css = 'badge badge-info fill-available text-white pointer-1'
                    elif(i.type_debts.name == 'Pagar'):
                        css = 'badge badge-warning fill-available text-dark pointer-1'
                    item['css'] = css
                    data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                client = Client.objects.using(db).filter(
                    names__icontains=term)[0:10]
                ci_client = Client.objects.using(
                    db).filter(ci__icontains=term)[0:10]
                providers = Providers.objects.using(
                    db).filter(names__icontains=term)[0:10]
                ci_providers = Providers.objects.using(
                    db).filter(ci__icontains=term)[0:10]
                for i in client:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + \
                        '-' + i.ci + ' (' + i.address+')'
                    item['type_client'] = 1
                    data.append(item)
                for i in ci_client:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + \
                        '-' + i.ci + ' (' + i.address+')'
                    item['type_client'] = 1
                    data.append(item)
                for i in providers:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + \
                        '-' + i.ci + ' (' + i.address+')'
                    item['type_client'] = 2
                    data.append(item)
                for i in ci_providers:
                    item = i.toJSON()
                    item['text'] = i.names + ' ' + i.identity.identity + \
                        '-' + i.ci + ' (' + i.address+')'
                    item['type_client'] = 2
                    data.append(item)
            elif action == 'addClient':
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
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo cliente')
            elif action == 'addCredit':
                perms = ['add_payments',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    d = Debts.objects.using(db).get(pk=request.POST['idCredit'])
                    dl = float(d.rate)
                    q = float(convertToDecimalFormat(request.POST['quantity']))

                    newDebts = float(d.dollars) - q
                    bs = newDebts * dl
                    d.dollars = newDebts
                    d.bs = bs
                    d.save(using=db)

                    image = ''
                    if not request.FILES:
                        image = 'Cap_Payments/empty.png'
                    else:
                        image = request.FILES['image']
                    dl = Payments()
                    dl.pay_date = request.POST['pay_date']
                    dl.provider = request.POST['provider']
                    dl.quantity = q
                    dl.description = request.POST['description']
                    dl.image = image
                    dl.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                    'Resgistró un nuevo abono de factura')
            elif action == 'addProvider':
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
                                    'Registró un nuevo Proveedor')
            elif action == 'add':
                perms = ['add_type_debts',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    with transaction.atomic():
                        dl = float(convertToDecimalFormat(request.POST['rate']))

                        pd = float(convertToDecimalFormat(request.POST['dollars']))
                        bs = pd * dl

                        if(request.POST['client'] == '1'):
                            client = Client.objects.using(db).get(
                                pk=request.POST['searchClient'])
                        elif(request.POST['client'] == '2'):
                            client = Providers.objects.using(db).get(
                                pk=request.POST['searchClient'])

                        debts = Type_debts.objects.using(db).get(
                            pk=request.POST['type_debts'])
                        if(debts.name == 'Cobrar'):
                            css = 'rgb(186, 139, 0)'
                        elif(debts.name == 'Pagar'):
                            css = 'rgb(15, 102, 116)'

                        description = request.POST['description']

                        d = Debts()
                        d.type_debts_id = debts.id
                        d.client = client.names + ' ' + client.ci + \
                            ' ' + client.address + ' ('+client.contact+')'
                        d.description = description
                        d.rate = dl
                        d.start_date = request.POST['start_date']
                        d.end_date = request.POST['end_date']
                        d.dollars = pd
                        d.bs = bs
                        d.save(using=db)
                        RegisterOperation(db, request.user.pk,
                                        'Resgistró una nueva cuenta por Cobrar/Pagar')

                        p = Permisology()
                        p.name = debts.name + ' a ' + client.names
                        p.description = description + \
                            ' (Monto: ' + request.POST['dollars'] + '$).'
                        p.day = request.POST['end_date']
                        p.color = css
                        p.save(using='default')
                        RegisterOperation(
                            db, request.user.pk, 'Registró en el calendario una cuenta por Cobrar/Pagar')
            elif action == 'edit':
                perms = ['change_debts',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    with transaction.atomic():
                        if not ',' in request.POST['rate']:
                            dl = float(request.POST['rate'])
                        else:
                            dl = float(convertToDecimalFormat(request.POST['rate']))

                        if not ',' in request.POST['dollars']:
                            pd = float(request.POST['dollars'])
                        else:
                            pd = float(convertToDecimalFormat(request.POST['dollars']))

                        bs = pd * dl

                        py_name = request.POST['client']
                        py_description = request.POST['description']
                        py_day = request.POST['end_date']

                        if Permisology.objects.using('default').filter(name=py_name, description=py_description, day=py_day).exists():
                            pass
                        else:
                            d = Debts.objects.using(db).get(pk=request.POST['id'])
                            py_name = d.client
                            py_description = d.description
                            py_day = d.end_date

                            Permisology.objects.using('default').filter(
                                name=py_name, description=py_description, day=py_day).delete()

                            type_debt = Type_debts.objects.using(
                                db).get(pk=request.POST['type_debts'])
                            if(type_debt.name == 'Cobrar'):
                                css = 'rgb(186, 139, 0)'
                            elif(type_debt.name == 'Pagar'):
                                css = 'rgb(15, 102, 116)'

                            p = Permisology()
                            p.name = request.POST['client']
                            p.description = request.POST['description']
                            p.day = request.POST['end_date']
                            p.color = css
                            p.save(using='default')

                        d = Debts.objects.using(db).get(pk=request.POST['id'])
                        d.type_debts_id = request.POST['type_debts']
                        d.client = request.POST['client']
                        d.description = request.POST['description']
                        d.rate = dl
                        d.start_date = request.POST['start_date']
                        d.end_date = request.POST['end_date']
                        d.dollars = pd
                        d.bs = bs
                        d.save(using=db)
                        RegisterOperation(
                            db, request.user.pk, 'Editó los datos de una cuenta por Cobrar/Pagar')
            elif action == 'delete':
                perms = ['delete_debts',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Debts.objects.using(db).get(pk=request.POST['id']).delete()
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cobrar/Pagar'
        context['list_url'] = reverse_lazy('crud:debts')
        context['dl'] = get_dollar()
        context['form'] = DebtsForm()
        context['formClient'] = ClientForm()
        context['formProviders'] = ProvidersForm()
        context['formDollar'] = PaymentsForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

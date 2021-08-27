from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.models import Shopping, Dolar
from mf.crud.forms import ShoppingForm
from mf.crud.functions import *


class ShoppingListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'shopping/list.html'
    permission_required = 'view_shopping'

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
                for i in Shopping.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_shopping', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.using(db).get(pk=1)
                    dl = float(dolar.dolar)
                    p = float(convertToDecimalFormat(
                        request.POST['amount_dl']))

                    iva = 1.16
                    bs = p * dl

                    s = Shopping()
                    s.date = request.POST['date']
                    s.concept = request.POST['concept']
                    s.amount_dl = p
                    s.amount_bs = bs
                    s.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                      'Registró una nueva compra')
            elif action == 'edit':
                perms = ['change_shopping', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    dolar = Dolar.objects.using(db).get(pk=1)
                    dl = float(dolar.dolar)
                    iva = 1.16

                    if not ',' in request.POST['amount_dl']:
                        p = float(request.POST['amount_dl'])
                    else:
                        p = float(convertToDecimalFormat(
                            request.POST['amount_dl']))

                    bs = p * dl

                    s = Shopping.objects.using(db).get(pk=request.POST['id'])
                    s.date = request.POST['date']
                    s.concept = request.POST['concept']
                    s.amount_dl = p
                    s.amount_bs = bs
                    s.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                      'Editó los datos de una compra')
            elif action == 'delete':
                perms = ['delete_shopping', ]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Shopping.objects.using(db).get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk,
                                      'Eliminó el registro de una compra')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compras'
        context['list_url'] = reverse_lazy('crud:shopping_list')
        context['dl'] = get_dollar()
        context['form'] = ShoppingForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

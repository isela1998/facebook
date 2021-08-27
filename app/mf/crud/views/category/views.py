from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from crum import get_current_request
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Category
from mf.crud.forms import CategoryForm
from mf.crud.functions import *

class CategoryListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'category/list.html'
    permission_required = 'view_category'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            db = 'default'
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.using(db).all():
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_category',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    ctg = Category()
                    ctg.name = request.POST['name']
                    ctg.save(using='default')
                    RegisterOperation(db, request.user.pk, 'Agregó una nueva Categoría de Producto')
            elif action == 'edit':
                perms = ['change_category',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    ctg = Category.objects.using(db).get(pk=request.POST['id'])
                    ctg.name = request.POST['name']
                    ctg.save(using='default')
                    RegisterOperation(db, request.user.pk, 'Editó una Categoría de Producto')
            elif action == 'delete':
                perms = ['delete_category',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    Category.objects.using('default').get(
                        pk=request.POST['id']).delete()
                    RegisterOperation(db, request.user.pk, 'Borró una Categoría de Producto')
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categorías'
        context['list_url'] = reverse_lazy('crud:category_list')
        context['dl'] = get_dollar()
        context['form'] = CategoryForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

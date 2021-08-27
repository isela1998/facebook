from django.shortcuts import render

# Create your views here.
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from mf.user.forms import UserForm
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from mf.crud.functions import *

from mf.user.models import User

class UserListView(TemplateView):
    # model = User
    template_name = 'user/list.html'
    permission_required = 'view_user', 'add_user', 'change_user', 'delete_user'

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
                for i in User.objects.all().exclude(pk=1):
                    data.append(i.toJSON())
            elif action == 'add':
                perms = ['add_user',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    if not request.FILES:
                        image = 'Users/empty.png'
                    else:
                        image = request.FILES['image']  
                    u = User()
                    u.first_name = request.POST['first_name']
                    u.last_name = request.POST['last_name']
                    u.username = request.POST['username']
                    u.set_password(request.POST['password'])
                    u.is_superuser = False
                    u.image = image
                    u.save()
                    u.groups.add(2)
            elif action == 'edit':
                perms = ['change_user',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    u = User.objects.get(pk=request.POST['id'])
                    if(u.pk == 2):
                        isSuperuser = True
                    else:
                        isSuperuser = False
                    if not request.FILES:
                        image = u.image
                    else:
                        image = request.FILES['image']  
                    u.first_name = request.POST['first_name']
                    u.last_name = request.POST['last_name']
                    u.username = request.POST['username']
                    u.set_password(request.POST['password'])
                    u.is_superuser = isSuperuser
                    u.image = image
                    u.save()
                    u.groups.clear()
                    if(isSuperuser == True):
                        u.groups.add(1)
                    elif(isSuperuser == False):
                        u.groups.add(2)
            elif action == 'delete':
                perms = ['delete_user',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    u = User.objects.get(pk=request.POST['id'])
                    if(u.pk == 2):
                        data['error'] = 'No se puede eliminar el Usuario Principal'
                        isSuperuser = True
                    else:
                        User.objects.using('default').get(pk=request.POST['id']).delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['list_url'] = reverse_lazy('user:users_list')
        context['dl'] = get_dollar()
        context['form'] = UserForm()
        return context

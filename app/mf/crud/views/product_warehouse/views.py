from django.views.generic import TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.forms import ProductForm, CategoryForm, TypeProductForm
from mf.crud.models import Product, Category, Product, Type_product
from mf.crud.functions import *

class ProductWarehouseListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'product_warehouse/list.html'
    permission_required = 'view_product'

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
                for i in Product.objects.using(db).all().exclude(product_group__id=1):
                    item = i.toJSON()
                    if(i.quantity < 21):
                        css = 'badge badge-danger fill-available text-dark pointer-1'
                    elif(i.quantity > 21):
                        css = 'badge badge-success fill-available text-dark pointer-1'
                    item['css'] = css
                    item['image'] = str(i.image)
                    data.append(item)
            elif action == 'add':
                perms = ['add_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    dolar = Dolar.objects.using(db).get(pk=1)
                    iva = float(1.16)

                    price_dl = float(convertToDecimalFormat(
                        request.POST['price_dl']))
                    cost = float(convertToDecimalFormat(request.POST['cost']))

                    price_bs = price_dl * float(dolar.dolar)
                    price = price_bs / iva

                    gain_margin = price_dl - cost

                    if not request.FILES:
                        image = 'Products/empty.png'
                    else:
                        image = request.FILES['image']
                    product = Product()
                    product.product_group_id = 2
                    product.category_id = request.POST['category']
                    product.type_product_id = request.POST['type_product']
                    product.code = request.POST['code']
                    product.product = request.POST['product']
                    product.quantity = request.POST['quantity']
                    product.cost = cost
                    product.price = price
                    product.price_dl = price_dl
                    product.price_bs = price_bs
                    product.gain = gain_margin
                    product.image = image
                    product.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                    'Registró un nuevo producto')
            elif action == 'addCategory':
                perms = ['add_category',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    ctg = Category()
                    ctg.name = request.POST['name']
                    ctg.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró una nueva categoría de producto')
            elif action == 'addType':
                perms = ['add_type_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    type_p = Type_product()
                    type_p.name = request.POST['name']
                    type_p.save(using='default')
                    RegisterOperation(db, request.user.pk,
                                    'Registró una nuevo tipo de producto')
            elif action == 'edit':
                perms = ['change_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    image = ''
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    if not request.FILES:
                        image = product.image
                    else:
                        image = request.FILES['image']

                    dolar = Dolar.objects.using(db).get(pk=1)
                    iva = float(1.16)

                    if "," not in request.POST['price_dl']:
                        price_dl = float(request.POST['price_dl'])
                    else:
                        price_dl = float(convertToDecimalFormat(
                            request.POST['price_dl']))

                    if "," not in request.POST['cost']:
                        cost = float(request.POST['cost'])
                    else:
                        cost = float(convertToDecimalFormat(request.POST['cost']))

                    price_bs = price_dl * float(dolar.dolar)
                    price = price_bs / iva

                    gain_margin = price_dl - cost

                    product.category = Category.objects.using(
                        db).get(pk=request.POST['category'])
                    product.type_product = Type_product.objects.using(
                        db).get(pk=request.POST['type_product'])
                    product.product = request.POST['product']
                    product.code = request.POST['code']
                    product.quantity = request.POST['quantity']
                    product.cost = cost
                    product.price_dl = price_dl
                    product.price = price
                    product.price_bs = price_bs
                    product.gain = gain_margin
                    product.image = image
                    product.save(using=db)
                    RegisterOperation(db, request.user.pk,
                                    'Editó los datos de un producto')
            elif action == 'up-stock':
                perms = ['change_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    product.product_group_id = 1
                    product.save()
            elif action == 'delete':
                perms = ['delete_product',]
                group = request.user.groups.first()
                authorized = ValidatePermissions(perms, group)
                if(authorized == False):
                    data['error'] = 'Disculpe, usted no tiene permisos para ejecutar esta acción'
                elif(authorized == True):
                    product = Product.objects.using(db).get(pk=request.POST['id'])
                    img = str(product.image)
                    if img == 'Products/empty.png':
                        pass
                    else:
                        remove(MEDIA_ROOT + img)
                    product.delete()
                    RegisterOperation(db, request.user.pk,
                                    'Eliminó un producto del almacén')
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos|Stock2'
        context['list_url'] = reverse_lazy('crud:almacen_list')
        context['dl'] = get_dollar()
        context['form'] = ProductForm()
        context['formCategory'] = CategoryForm()
        context['formType'] = TypeProductForm()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

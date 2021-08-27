from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import transaction
import json

from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from mf.crud.forms import ProductForm, CategoryForm, TypeProductForm, ProductForm
from mf.crud.models import Product, Category, Type_product, Product, Dolar, CompanySedes
from mf.crud.functions import *

import os
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings
from xhtml2pdf import pisa
from datetime import date


class GainMaginListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'gainMargin/list.html'
    permission_required = 'view_product', 'add_product', 'change_product', 'delete_product'

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
                for i in Product.objects.using(db).all():
                    item = i.toJSON()
                    if(i.quantity < 21):
                        css = 'badge badge-danger fill-available text-dark pointer-1'
                    elif(i.quantity > 21):
                        css = 'badge badge-success fill-available text-dark pointer-1'
                    item['css'] = css
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Margen de Ganancias'
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

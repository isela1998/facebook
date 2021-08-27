from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import Product
from mf.crud.functions import *

class FewProductsListView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'few_products/list.html'
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
                for i in Product.objects.using(db).filter(quantity__lt=5):
                    data.append(i.toJSON())
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Poco Inventario'
        context['dl'] = get_dollar()
        context['list_url'] = reverse_lazy('crud:few_products')
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

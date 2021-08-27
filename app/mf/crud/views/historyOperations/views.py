from mf.user.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from config.settings import MEDIA_URL, STATIC_URL, MEDIA_ROOT
from os import remove

from django.contrib.auth.mixins import LoginRequiredMixin
from mf.crud.mixins import IsSuperuserMixin, ValidatePermissionMixin

from mf.crud.models import HistoryOperations
from mf.crud.functions import *


class HistoryOperationsView(LoginRequiredMixin, ValidatePermissionMixin, TemplateView):
    template_name = 'historyOperations/list.html'
    permission_required = 'view_historyoperations', 'add_historyoperations', 'change_historyoperations', 'delete_historyoperations'

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
                for i in HistoryOperations.objects.using(db).all():
                    user = User.objects.filter(pk=i.userSession.pk)
                    for u in user:
                        item = u.toJSON()
                        history = {
                            'datejoined': i.datejoined,
                            'user': i.userSession.username,
                            'name': item['full_name'],
                            'action': i.description
                        }
                        data.append(history)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Historial'
        context['list_url'] = reverse_lazy('crud:historyOperations')
        context['dl'] = get_dollar()
        context['events'] = get_events_today()
        context['q_events'] = get_q_events_today
        return context

from django.urls import path
from mf.reports.views import ReporteSaleView

urlpatterns = [
    # Reports
    path('sale/', ReporteSaleView.as_view(), name='sale_report')
]
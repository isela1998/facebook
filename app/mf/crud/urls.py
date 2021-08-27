from django.urls import path
from mf.crud.views.dollarHistory.views import *
from mf.crud.views.company.views import *
from mf.crud.views.category.views import *
from mf.crud.views.type.views import *
from mf.crud.views.requested.views import *
from mf.crud.views.product.views import *
from mf.crud.views.calendar.views import *
from mf.crud.views.few_products.views import *
from mf.crud.views.permisology.views import *
from mf.crud.views.method.views import *
from mf.crud.views.product_warehouse.views import *
from mf.crud.views.client.views import *
from mf.crud.views.providers.views import *
from mf.crud.views.facilitator.views import *
from mf.crud.views.debts.views import *
from mf.crud.views.cancelledInvoices.views import *
from mf.crud.views.payments.views import *
from mf.crud.views.expenses. views import *
from mf.crud.views.earnings. views import *
from mf.crud.views.shopping. views import *
from mf.crud.views.sale.views import *
from mf.crud.views.budget.views import *
from mf.crud.views.gainMargin.views import *
from mf.crud.views.salesSummary.views import *
from mf.crud.views.bankAccounts.views import *
from mf.crud.views.bankTransfers.views import *
from mf.crud.views.dashboard.views import *
from mf.crud.views.invoices.views import *
from mf.crud.views.type_services.views import *
from mf.crud.views.services.views import *
from mf.crud.views.historyOperations.views import *
# from mf.crud.views.tests.views import TestView

app_name = 'crud'

urlpatterns = [
    # Dollar History
    path('dollarHistory/list/', DollarHistoryView.as_view(), name='dollarHistory'),
    # Company
    path('company/list/', CompanyListView.as_view(), name='company'),
    # Category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    # Type
    path('type/list/', TypeListView.as_view(), name='type_list'),
    # Type
    path('typeServices/list/', TypeServicesListView.as_view(), name='type_services_list'),
    # Pay Method
    path('method/list/', MethodListView.as_view(), name='method_list'),
    # Invoices
    path('invoices/list/', InvoicesView.as_view(), name='invoices'),
    path('invoices/report/pdf/<int:s>/', InvoicesPdfView.as_view(), name='invoice_pdf'),
    # Products
    path('product/list/', ProductWarehouseListView.as_view(), name='product_list'),
    # Warehouse
    path('almacen/list/', ProductListView.as_view(), name='almacen_list'),
    # Products
    path('gainMargin/list/', GainMaginListView.as_view(), name='gain_list'),
    # Few_inventary
    path('inventary/list/', FewProductsListView.as_view(), name='few_products'),
    # Calendar
    path('calendar/list/', PermisologyListView.as_view(), name='calendar'),
    # Products
    path('requested/list/', RequestedView.as_view(), name='requested_list'),
    # Clients
    path('client/', ClientView.as_view(), name='client'),
    # Providers
    path('providers/', ProvidersView.as_view(), name='providers'),
    # Facilitator
    path('facilitator/', FacilitatorView.as_view(), name='facilitators'),
    # Debts
    path('debts/', DebtsListView.as_view(), name='debts'),
    # Cancelled Invoices
    path('cancelledInvoices/', CancelledInvoicesView.as_view(), name='cancelledInvoices'),
    # Payments
    path('payments/', PaymentsView.as_view(), name='payments'),
    # Expenses
    path('expenses/', ExpensesListView.as_view(), name='expenses_list'),
    # Earnigns
    path('earnings/', EarningsListView.as_view(), name='earnings_list'),
    # Shopping
    path('shopping/', ShoppingListView.as_view(), name='shopping_list'),
    # Services
    path('services/', ServicesListView.as_view(), name='services_list'),
    # Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/add/<int:pk>/', SaleDuplicateView.as_view(), name='sale_update'),
    # path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/invoice/pdf/<int:s>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # Budgets
    path('budgets/list/', BudgetListView.as_view(), name='budgets'),
    path('sale/budget/pdf/<int:s>/', BudgetPdfView.as_view(), name='budget_pdf'),
    # Sales Summary
    path('summary/list/', SalesSummaryListView.as_view(), name='summary_list'),
    # Bank Accounts
    path('bankAccounts/list/', BankAccountsView.as_view(), name='bankAccounts'),
    # Bank Transfers
    path('bankTransfers/list/', BankTransfersView.as_view(), name='bankTransfers'),
    # Inventary
    path('inventary/report/pdf/<int:i>/', InventaryPdfView.as_view(), name='inventary_pdf'),
    # Operations History
    path('operationsHistory/list/', HistoryOperationsView.as_view(), name='historyOperations'),
]



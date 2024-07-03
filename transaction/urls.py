from django.urls import path
from.views import transaction_view, delete_transaction,get_transaction_data

urlpatterns = [
    path('', transaction_view, name='transaction'),
    path('transaction/<int:pk>/delete/', delete_transaction, name='delete_transaction'),
    path('transaction/chart-data/', get_transaction_data, name='chart_data'),
]
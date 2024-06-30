from django.urls import path
from.views import transaction_view, delete_transaction

urlpatterns = [
    path('', transaction_view, name='transaction'),
    path('transaction/<int:pk>/delete/', delete_transaction, name='delete_transaction'),
    # path('chart-data/', get_chart_data, name='chart_data'),
]
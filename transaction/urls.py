from django.urls import path
from .views import transaction_view, delete_transaction


urlpatterns = [
    path('', transaction_view, name='transaction'),
    path('transaction/<pk>/delete/', delete_transaction, name='delete_transaction'),
    # ...
]

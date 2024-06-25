from django.urls import path
from .views import transaction_view
from . import views

urlpatterns = [
    path('', transaction_view, name='transaction'),
     path('transaction/<pk>/delete/', views.delete_transaction, name='delete_transaction'),
]

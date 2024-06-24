from django.urls import path
from .views import transaction_view

urlpatterns = [
    path('', transaction_view, name='transaction'),
]

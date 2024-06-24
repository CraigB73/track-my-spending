from django.urls import path
from .views import budget_view

urlpatterns = [
    path('', budget_view, name='budget'),
]

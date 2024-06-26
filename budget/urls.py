from django.urls import path
from .views import budget_view, delete_budget, update_budget

urlpatterns = [
    path('', budget_view, name='budget'),
    path('budgets/<pk>/delete/', delete_budget, name='delete_budget'),
    path('update_budget/<pk>/', update_budget, name='update_budget'),
]

from django.urls import path
from .views import BudgetView, DeleteBudgetView, UpdateBudgetView

urlpatterns = [
    path('', BudgetView.as_view(), name='budget'),
    path('budgets/<pk>/delete/', DeleteBudgetView.as_view(), name='delete_budget'),
    path('update_budget/<pk>/', UpdateBudgetView.as_view(), name='update_budget'),
]
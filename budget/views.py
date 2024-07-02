from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.views.generic import View, UpdateView, DeleteView
from.forms import BudgetForm
from.models import Budget

class BudgetView(View):
    template_name = "budget/budget.html"
    form_class = BudgetForm
    """
    Gets the budget model obj. If budget obj exist.
    Check the current month/year to ensure user only creates one budget the existing month.
    Retrieved save budget data to be displayed in budget tempalates
    """
    def get(self, request):
        current_month = datetime.now().month
        current_year = datetime.now().year

        existing_budget = Budget.objects.filter(user=request.user, created_on__year=current_year, created_on__month=current_month).exists()

        if existing_budget:
            budgets = Budget.objects.filter(user=request.user, created_on__year=current_year, created_on__month=current_month)
            form = self.form_class(instance=budgets.first())
        else:
            form = self.form_class()

        budgets = Budget.objects.filter(user=request.user).order_by("-created_on")
        total_income = self.calculate_totals('income', budgets)
        total_expenses = self.calculate_totals('expense', budgets)
        total_monthly_savings = self.calculate_totals('monthly_saving', budgets)
        total_allowance = self.calculate_totals('allowance', budgets)
        total_goal_savings = self.calculate_totals('goal_saving', budgets)
        goal_saving_item = [budget.goal_saving_item for budget in budgets]

        return render(request, self.template_name, {
            "form": form,
            "budgets": budgets,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "total_monthly_savings": total_monthly_savings,
            "total_allowance": total_allowance,
            "total_goal_savings": total_goal_savings,
            "goal_saving_item": goal_saving_item,
            "saved": True
        })
        
        
    """
    Checks for existiing current month budget.
    Displays message if User tries to create a budget in the curret month more that once.
    """    
    def post(self, request):
        current_month = datetime.now().month
        current_year = datetime.now().year

        existing_budget = Budget.objects.filter(user=request.user, created_on__year=current_year, created_on__month=current_month).exists()

        if existing_budget:
            messages.error(request, "You can only create one monthly budget. You are able to update your current budget if needed.")
            return redirect("budget")

        form = self.form_class(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("budget")


    """
    Use Budget calculate totals within the above get() method.
    """
    def calculate_totals(self, field, budgets):
        return sum(getattr(budget, field) if getattr(budget, field) is not None else 0 for budget in budgets)


class DeleteBudgetView(DeleteView):
    model = Budget
    success_url = reverse_lazy("budget")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj


class UpdateBudgetView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budget/update_budget.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return reverse_lazy("budget")
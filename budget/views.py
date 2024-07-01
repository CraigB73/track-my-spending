from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import BudgetForm
from .models import Budget

# Create your views here.

@login_required
def budget_view(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect("budget")
    else:
        form = BudgetForm()
       
    budgets = Budget.objects.filter(user=request.user).order_by("-created_on") 
    # Calculate input totals to redender in a list
    total_income = calculate_totals('income', budgets)
    total_expenses = calculate_totals('expense', budgets)
    total_monthly_savings = calculate_totals('monthly_saving', budgets)
    total_allowance = calculate_totals('allowance', budgets)
    total_goal_savings = calculate_totals('goal_saving', budgets)
    goal_saving_item = [budget.goal_saving_item for budget in budgets] 
    
    return render(request, "budget/budget.html", {
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
    
    
def calculate_totals(field, budgets):
        return sum(getattr(budget, field) if getattr(budget, field) is not None else 0 for budget in budgets)

@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    budget.delete()
    return redirect(reverse_lazy("budget"))

@login_required
def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = Budget.objects.get(id=request.user.id)  # assuming the budget is associated with the user
            budget.income = form.cleaned_data['income']
            budget.expense = form.cleaned_data['expense']
            budget.allowance = form.cleaned_data['allowance']
            budget.monthly_saving = form.cleaned_data['monthly_saving']
            budget.goal_saving = form.cleaned_data['goal_saving']
            budget.goal_saving_item = form.cleaned_data['goal_saving_item']
            budget.save()
            return redirect('budget') 
    else:
        form = BudgetForm(instance=budget)  
    return render(request, "budget/update_budget.html", {"form": form})


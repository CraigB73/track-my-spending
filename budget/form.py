from .models import Budget
from django import forms

class BudgetForm(forms.ModelForm):
    model = Budget
    fields = [
        "income",
        "expense", 
        "allowance", 
        "monthly_saving", 
        "goal_saving", 
        "goal_saving_item"
    ]
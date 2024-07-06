from .models import Budget
from django import forms

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            "income",
            "expense", 
            "allowance", 
            "monthly_saving", 
            "goal_saving", 
            "goal_saving_item"
        ]
        widgets = {
            "income": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter income", "autocomplete": "off", "required": "" }),
            "expense": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter expense", "autocomplete": "off" }),
            "allowance": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter allowance","autocomplete": "off",  "required": "" }),
            "monthly_saving": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter monthly saving", "autocomplete": "off" }),
            "goal_saving": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter goal saving", "autocomplete": "off" }),
            "goal_saving_item": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter goal saving item"}),
        }
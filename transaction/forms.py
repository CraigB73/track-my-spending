from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ["transaction_amount", "location", "category"]
    widgets = {
        "transaction_amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter amount"}),
        "category": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter category"}),
        "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter location", "required":"required"}),
    }
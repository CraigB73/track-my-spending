from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ["transaction_amount", "location", "category"]
    widget = {
      "transaction_amount": forms.TextInput(attrs={"class": "form-control"}),  
      "category": forms.TextInput(attrs={"class": "form-control"}),
    }
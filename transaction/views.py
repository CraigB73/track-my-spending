from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Transaction, Budget
from .forms import TransactionForm

# Create your views here.
@login_required
def transaction_view(request):   
    #Gets the allowance created in the Budget model for authorized user
    try:
        budget = Budget.objects.get(user=request.user)
    except Budget.DoesNotExist:
        return render(request, 'transaction/transaction.html')
    allowance = budget.allowance
    budget.save()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction')
    
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.filter(user = request.user).order_by("-created_on")
    total_transactions = sum(transaction.transaction_amount for transaction in transactions )
    
    allowance_remaining = allowance - total_transactions
    
    list_transactions = []
    for transaction in transactions:
        list_transactions.append({
            "transaction": transaction,
            "amount": transaction.transaction_amount,
            "location": transaction.location,
            "category": transaction.category
        })
        
  
    return render(request, 'transaction/transaction.html', {
            "form": form,
            "allowance": allowance,
            "transactions": transactions,
            "total_transaction": total_transactions,
            "remaining_allowance": allowance_remaining,
            "list_transactions": list_transactions,
            "saved": True
            })

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    return redirect(reverse_lazy("transaction"))

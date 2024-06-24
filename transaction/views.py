from django.shortcuts import render, redirect, get_list_or_404
from .models import Transaction, Budget
from django.urls import reverse_lazy
from .forms import TransactionForm


# Create your views here.
def transaction_view(request):
    try:
        budget = Budget.objects.get(user=request.user)
    except Budget.DoesNotExist:
        return render(request, 'transaction/transactions.html')
    allowance = budget.allowance
    budget.save()
    
    if request.methond == "POST":
        form = TransactionForm(request.POST)
        transaction = form.save(Commit=False)
        transaction.save()
        return redirect('transaction')
    
    else: 
        form = TransactionForm()
        
    transactions = Transaction.objects.filter(user = request.user).order_by("_created_on")
    # Provides the purnchase transaction use to subtract from users allowance
    total_transactions = sum(transaction.transaction_amount for transaction in transactions)
    
    # Calculates remaining allowance 
    alllowance_remaining = allowance - total_transactions
    
    """
    Creates a list to be render in transaction template
    """
    list_transactions = []
    for transaction in transactions:
        list_transactions.append({
            "transaction": transaction,
            "amount": transaction.transaction_amount,
            "location": transaction.location,
            "category": transaction.category,
        })
    
    return render(request, "transaction/transaction.html", {
        "form": form,
        "allowance": allowance,
        "transactions": transactions,
        "total_transactions": total_transactions,
        "remaining_allowance": alllowance_remaining,
        "list_transactions": list_transactions,
        "saved": True,
    })
    

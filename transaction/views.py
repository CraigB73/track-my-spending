from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Transaction, Budget
from .forms import TransactionForm
from django.views.decorators.http import require_GET
from django.db.models import Sum

# Create your views here.
@login_required
def transaction_view(request): 
    #Queries the budget model to use allowance created within the budget  
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
    
    
    global allowance_remaining #Enable to use varible in delete_transaction to add back transaction
    allowance_remaining = allowance - total_transactions
    
    """
    Creates a list to be render in the table
    """
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
"""
Upond deletion transaction will be removed from table row and update 
the allowance by returning the transaction amount back to remaining_allowance"""
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    budget = Budget.objects.get(user=request.user)
    if ( allowance_remaining < budget.allowance ):
        transaction.transaction_amount += allowance_remaining
    budget.save()
    transaction.delete()
    return redirect(reverse_lazy("transaction"))


"""
Retrieves data from the transaction model which is used to 
dynamically updated the Chart.js pie chart.
"""
@require_GET
@login_required
def get_transaction_data(request):
    transactions = Transaction.objects.filter(user=request.user)
    # Get each cateory and totals the transactions of that each category(with help of ChatGPT)
    aggregated_data = transactions.values('category').annotate(total_amount=Sum('transaction_amount'))
    #Creates obj of list to be passed to pie chart
    transaction_data = {
        'labels': [data['category'] for data in aggregated_data],
        'data': [data['total_amount'] for data in aggregated_data]
    }
    
    return JsonResponse(transaction_data)#return a JSON reponse when making an API call in transaction_script.js
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import F, Sum
from django.views.decorators.http import require_POST
from .models import Budget, Transaction
from .forms import TransactionForm

def transaction_view(request):
    try:
        budget = Budget.objects.get(user=request.user)
    except Budget.DoesNotExist:
        return render(request, 'transaction/transaction.html')
    allowance = budget.allowance

    budget.save()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            amount = form.cleaned_data['transaction_amount']

            existing_transaction = Transaction.objects.filter(user=request.user, category=category).first()
            if existing_transaction:
                existing_transaction.transaction_amount = F('transaction_amount') + amount
                existing_transaction.save()
            else:
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
            
            return JsonResponse({'status': 'success'})

    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by("-created_on")
    total_transactions = sum(transaction.transaction_amount for transaction in transactions)
    allowance_remaining = allowance - total_transactions

    return render(request, 'transaction/transaction.html', {
        "form": form,
        "allowance": allowance,
        "transactions": transactions,
        "total_transaction": total_transactions,
        "remaining_allowance": allowance_remaining,
        'delete_transaction_url': reverse_lazy('delete_transaction', args=[1]),  # Correct placeholder
        "saved": True
    })
    
def get_chart_data(request):
    transactions = Transaction.objects.filter(user=request.user)
    categories = transactions.values('category').annotate(total_amount=Sum('transaction_amount'))
    data = {
        'labels': [category['category'] for category in categories],
        'data': [float(category['total_amount']) for category in categories],
    }
    return JsonResponse(data)

@require_POST
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    budget = Budget.objects.get(user=request.user)
    budget.allowance += transaction.transaction_amount
    budget.save()
    transaction.delete()
    
    return JsonResponse({'status': 'success'})
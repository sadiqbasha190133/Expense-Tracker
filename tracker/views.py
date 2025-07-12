from django.shortcuts import render, redirect
from tracker.models import TrackingHistory, CurrentBalance
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method =='POST':
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))
        
        print(description, amount)

        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        expense_type = "CREDIT"
        if amount < 0:
            expense_type = "DEBIT"
        
        if amount == 0:
            messages.warning(request, "Amount should not be 0")
            return redirect("/")

        tracking_history = TrackingHistory.objects.create(
            amount = amount,
            description = description,
            expense_type = expense_type,
            current_balance = current_balance,
        )
        current_balance.current_balance += amount
        current_balance.save()
        return redirect('/')
    
    transactions = TrackingHistory.objects.all()

    income, expenses = 0.0, 0.0
    for transaction in transactions:
        if transaction.expense_type == "CREDIT":
            income += transaction.amount
        else:
            expenses += transaction.amount


    current_balance = CurrentBalance.objects.get(id = 1)
    context = {
        "transactions":transactions,
        "balance":current_balance,
        "income":income,
        "expenses":expenses
    }
    return render(request, "index.html", context)


def deleteTransaction(request, id):
    transaction_history = TrackingHistory.objects.filter(id = id)
    balance = CurrentBalance.objects.get(id = 1)
    balance.current_balance -= transaction_history[0].amount
    balance.save()
    transaction_history.delete()
    return redirect('/')



from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
import json

# Create your views here.
def home(request):
    if request.user.is_authenticated:
       
        
        # user=User.objects.get()
        expense=request.user.expense_set.all()
        income=request.user.income_set.all()
        expense_summary= request.user.expensesummary_set.all()
        # expense_summary.update_expense_summary()
        income_summary= request.user.incomesummary_set.all()
        # for chart
        
        context={
            'expense':expense,
            'income':income,
            'expense_summary':expense_summary,
            'income_summary':income_summary
            }
        
        # print(context)
        # print(expense_summary,income_summary)
        if request.user.is_authenticated:
            return render(request, 'core/home.html',context)
        else:
            return render(request, 'login/login.html')
    else:
        return render(request, 'core/home.html')
def expense(request): 
    if request.method == 'POST':
        name=request.POST['name']
        amount=request.POST['amount']
        description=request.POST['description']
        cat=request.POST.get('category')
        category=ExpenseCategory.objects.get(name=cat)
      
        expense=Expense(user=request.user,name=name,amount=amount,description=description,category=category)
        expense.save()
       
        return redirect('expense')
    else:
        expense=request.user.expense_set.all()
        expense_category=ExpenseCategory.objects.all()
        content_send={
            'expense':expense,
            'expense_category':expense_category
        }
       
        return render(request, 'core/expences.html',content_send)
    
def income(request):
    if request.method == 'POST':
        name=request.POST['name']
        amount=request.POST['amount']
        description=request.POST['description']
        cat=request.POST.get('category')
        category=IncomeCategory.objects.get(name=cat)
        income=Income(user=request.user,name=name,amount=amount,description=description,category=category)
        income.save()
        return redirect('income')
    else:
        income=request.user.income_set.all()
        income_category=IncomeCategory.objects.all()
        content_send={
            'incomes':income,
            'income_category':income_category
        }
        return render(request, 'core/income.html',content_send)

def update_expense(request,expense_id):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        description = request.POST['description']
        cat = request.POST.get('category')
        
        category = ExpenseCategory.objects.get(id=cat)
        expense = Expense.objects.get(id=expense_id)
        expense.name = name
        expense.amount = amount
        description = description
        expense.category = category
        expense.save()
        
        
       
        
        return redirect('expense')
    else:
        expense=Expense.objects.get(id=expense_id)
        expense_category=ExpenseCategory.objects.all()
        content_send={
            'expense':expense,
            'expense_category':expense_category
        }
        return render(request, 'core/update_expense.html',content_send)
# views.py




def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    print(expense_id)
    expense.delete()
    return redirect('expense')  # Redirect to the page with the expense list
    # return render(request, 'confirm_delete.html', {'expense': expense})

def delete_income(request, incom_id):
    print(incom_id)
    income = get_object_or_404(Income, id=incom_id)
    
    income.delete()
    return redirect('income')

def update_income(request, incom_id):
    print(incom_id)
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        description = request.POST['description']
        cat = request.POST.get('category')

        category = IncomeCategory.objects.get(id=cat)
        income = Income.objects.get(id=incom_id)
        income.name = name
        income.amount = amount
        description = description
        income.category = category
        income.save()




        return redirect('income')
    else:
        income=Income.objects.get(id=incom_id)
        income_category=IncomeCategory.objects.all()
        content_send={
            'income':income,
            'income_category':income_category
        }
        return render(request, 'core/update_income.html',content_send)
    
from django.core.serializers.json import DjangoJSONEncoder
def expense_summary(request):
    # Fetch data from the database
    expense_summary = ExpenseSummary.objects.filter(user=request.user)

    # Extract categories and totals
    categories = [item.category.name for item in expense_summary]  # Assuming category has a name attribute
    totals = [float(item.total_expenses) for item in expense_summary]  # Convert Decimal to float

    # Prepare context
    context = {
        'categories_json': json.dumps(categories, cls=DjangoJSONEncoder),
        'totals_json': json.dumps(totals, cls=DjangoJSONEncoder),
        'expense_summary': expense_summary
    }
    return render(request, 'core/expense_summary.html', context)
def income_summary(request):
    # Fetch data from the database
    income_summary = IncomeSummary.objects.filter(user=request.user)
    # Extract categories and totals
    categories = [item.category.name for item in income_summary]  # Assuming category has a name attribute
    totals = [float(item.total_income) for item in income_summary]  # Convert Decimal to float
    # Prepare context
    context = {
        'categories_json': json.dumps(categories, cls=DjangoJSONEncoder),
        'totals_json': json.dumps(totals, cls=DjangoJSONEncoder),
        'income_summary': income_summary
    }
    return render(request, 'core/income_summary.html', context)
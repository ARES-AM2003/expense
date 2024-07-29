from django.contrib import admin
from .models import Expense, Income, ExpenseCategory, ExpenseSummary, IncomeCategory,IncomeSummary
# Register your models here.

admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSummary)
admin.site.register(IncomeCategory)
admin.site.register(IncomeSummary)

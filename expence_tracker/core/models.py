from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField()
    category = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField()
    category = models.ForeignKey('IncomeCategory', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Expense Categories"

    def __str__(self):
        return self.name

class ExpenseSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Expense Summaries"
        # unique_together = ('user', 'category')

    def __str__(self):
        return f"Expense Summary for {self.user.username} - {self.category.name}"

    def update_summary(self):
        self.total_expenses = self.user.expense_set.filter(category=self.category).aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.save()


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Income Categories"

    def __str__(self):
        return self.name
    

class IncomeSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Income Summaries"
        unique_together = ('user', 'category')

    def __str__(self):
        return f"Income Summary for {self.user.username} - {self.category.name}"

    def update_summary(self):
        self.total_income = self.user.income_set.filter(category=self.category).aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.save()
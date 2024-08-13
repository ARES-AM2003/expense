from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
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
        unique_together = ('user', 'category')

    def __str__(self):
        return f" {self.category.name} --- {self.total_expenses}"

    def update_summary(self):
        # Calculate the total expenses for this user and category
        total = Expense.objects.filter(user=self.user, category=self.category).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        if self.total_expenses != total:
            self.total_expenses = total
            self.save()

        
    
@receiver(post_save, sender=Expense)
def update_expense_summary(sender, instance, **kwargs):
    # Handle the case where multiple ExpenseSummary instances might exist for a user and category
    summaries = ExpenseSummary.objects.filter(user=instance.user, category=instance.category)
    if not summaries.exists():
        # Create a new summary if it doesn't exist
        ExpenseSummary.objects.create(
            user=instance.user,
            category=instance.category
        ).update_summary()
    else:
        for summary in summaries:
            summary.update_summary()
@receiver(post_delete, sender=Expense)
def update_expense_summary_on_delete(sender, instance, **kwargs):
    summaries = ExpenseSummary.objects.filter(user=instance.user, category=instance.category)
    for summary in summaries:
        summary.update_summary()
    

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


@receiver(post_save, sender=Income)
def update_income_summary(sender, instance, **kwargs):
    # Handle the case where multiple IncomeSummary instances might exist for a user and category
    summaries = IncomeSummary.objects.filter(user=instance.user, category=instance.category)
    
    if not summaries.exists():
        # Create a new summary if it doesn't exist
        IncomeSummary.objects.create(
            user=instance.user,
            category=instance.category
        ).update_summary()
    else:
        for summary in summaries:
            summary.update_summary()


@receiver(post_delete, sender=Income)
def update_income_summary_on_delete(sender, instance, **kwargs):
    summaries = IncomeSummary.objects.filter(user=instance.user, category=instance.category)
    for summary in summaries:
        summary.update_summary()

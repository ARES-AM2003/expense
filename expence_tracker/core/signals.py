# core/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, ExpenseSummary

@receiver(post_save, sender=Expense)
@receiver(post_delete, sender=Expense)
def update_expense_summary(sender, instance, **kwargs):
    summaries = ExpenseSummary.objects.filter(user=instance.user, category=instance.category)
    for summary in summaries:
        summary.update_summary()

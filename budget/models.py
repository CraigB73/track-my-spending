from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
Create budget to track monthly living cost and create a saving plan
"""
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budget", null=True)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_saving = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    goal_saving = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    goal_saving_item =models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]
        
    def __str__(self):
        return f"{self.income} - {self.allowance} - {self.expense} - {self.monthly_saving} - {self.goal_saving} - {self.goal_saving_item}"

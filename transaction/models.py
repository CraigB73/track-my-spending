from django.db import models
from django.contrib.auth.models import User


# Create your models here.
'''
Used to track and save transaction details
'''
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction", null=True, blank=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=150, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f" {self.transaction_amount} -  {self.location} - {self.category} - {self.created_on}"
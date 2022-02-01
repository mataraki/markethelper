from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    pass
    iextoken = models.TextField(blank=False)
    invested = models.DecimalField(blank=False, default=0, decimal_places=2, max_digits=10)

class Share(models.Model):
    owner =  models.ForeignKey("User", on_delete=models.CASCADE, related_name="ownings")
    type = models.TextField(blank=False)
    ticker = models.TextField(blank=False)
    name = models.TextField(blank=False, default=ticker)
    quantity = models.IntegerField(blank=False, default=1)
    pricebought = models.DecimalField(blank=False, decimal_places=2, max_digits=7)
    pricecurrent = models.DecimalField(blank=False, decimal_places=2, max_digits=7)
    currency = models.TextField(blank=False)
    rating = models.IntegerField(blank=False, validators = [MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "ticker": self.ticker,
            "name": self.name,
            "quantity": self.quantity,
            "pricebought": self.pricebought,
            "pricecurrent": self.pricecurrent,
            "currency": self.currency,
            "rating": self.rating,
            "notes": self.notes
        }

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255,null=True,blank=True)
    share_related = models.ForeignKey("Share", blank=True, null=True, on_delete=models.CASCADE, related_name="shares")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.event_name
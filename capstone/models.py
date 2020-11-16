from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Merchandise(models.Model):

    currency_categories = [ ("USD", "United States Dollar"), ("BOB", "Boliviano"), ("EUR", "Euro") ]

    user = models.ForeignKey(User, related_name="merchandises", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    title = models.CharField(max_length=64)
    description = models.TextField()
    quantity = models.IntegerField()
    currency = models.CharField(max_length=3, choices=currency_categories, default="USD")
    acquisition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        unique_together = ('user', 'code',)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "code": self.code,
            "title": self.title,
            "description": self.description,
            "quantity": self.quantity,
            "currency": self.currency,
            "acquisition_date": self.acquisition_date.strftime("%b %d %Y, %I:%M %p"),
            "total_acquisition_cost": self.calculate_total_acquisition_cost(),
            "acquisition_costs": [cost.serialize() for cost in self.costs.all()]
        }
    
    def calculate_total_acquisition_cost(self):
        total = 0
        for cost in self.costs.all():
            total += cost.cost
        return total

class AcquisitionCost(models.Model):
    merchandise = models.ForeignKey(Merchandise, related_name="costs", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField()
    cost = models.DecimalField(max_digits=64, decimal_places=2)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cost": self.cost
        }

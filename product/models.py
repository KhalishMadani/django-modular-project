from django.db import models
from django.db.models import JSONField

# Create your models here.
class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    dynamic_fields = JSONField(default=dict)

    def __str__(self):
        return self.name
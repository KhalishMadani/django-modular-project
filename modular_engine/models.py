from django.db import models

# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=50, unique=True)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name
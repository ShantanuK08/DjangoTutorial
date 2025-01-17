from django.db import models

# Create your models here.
# models.py
from django.db import models

class Post(models.Model):
    reference_number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    idproof = models.CharField(max_length=50)

    def __str__(self):
        return self.name

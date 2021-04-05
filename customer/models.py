from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.utils.timezone import now
from model_utils import Choices
# Create your models here.

class Customer(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    create_date = models.DateField(default=now)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    company_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    GENDER = Choices(
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(max_length=100, choices=GENDER, default='male')
    STATUS = Choices(
        ('single', 'Single'),
        ('married', 'Married')
    )
    status = models.CharField(max_length=100, choices=STATUS, default='single')
    age = models.CharField(max_length=10)
    income_int = models.CharField(max_length=100)
    income = models.CharField(max_length=100)

    class Meta:
        ordering: ['-create_date']
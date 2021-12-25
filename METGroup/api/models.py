from typing import Any
from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=150)

    def __str__(self):
        return '{0}'.format(self.name)

class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=150)
    price = models.FloatField('price', max_length=50)
    storeId = models.ForeignKey(Store,related_name='items',on_delete=models.CASCADE)

    def __str__(self):
        return '{0},{1},{2}'.format(self.name, self.price, self.storeId)
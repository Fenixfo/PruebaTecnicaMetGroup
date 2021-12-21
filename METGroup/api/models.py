from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=150)
    price = models.FloatField('price', max_length=50)

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.price)
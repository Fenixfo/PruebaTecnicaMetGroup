from django.contrib import admin
from .models import Items, Store

admin.site.register(Store)
admin.site.register(Items)
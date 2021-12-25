from django.db.models import fields
from rest_framework import serializers
from .models import Items, Store

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = "__all__"

class StoreSerializer(serializers.ModelSerializer):
    items=ItemsSerializer(read_only=True, many=True)
    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'items',
        )


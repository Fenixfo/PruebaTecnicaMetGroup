from django.urls import path
from .views import StoreList

urlpatterns = [
    path('store/', StoreList.as_view(), name='store_list'),
]
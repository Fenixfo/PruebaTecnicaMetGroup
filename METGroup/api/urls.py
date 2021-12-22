from django.urls import path
from .views import StoreList
from . import views

urlpatterns = [
    path('store/', StoreList.as_view(), name='store_list'),
    path('auth/', views.auth),
    path('register/', views.register),
]

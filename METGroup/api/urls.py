from django.urls import path
from django.urls.conf import include
from .views import ItemView, ItemsList, StoreList, StoreView, StoreViewAll
from . import views

urlpatterns = [
    path('storesOriginal/', StoreList.as_view(), name='store_list'),
    path('itemsOriginal/', ItemsList.as_view(), name='items_list'),
    path('auth', views.auth),
    path('register', views.register),
    # path('api/', include('api.urls'))
    # path('store/<str:name>', views.newStore),
    path('store/<str:name>', StoreView.as_view(), name='store_process'),
    path('item/<str:name>', ItemView.as_view(), name='item_process'),
    path('stores/', StoreViewAll.as_view(), name='stores_process'),
    # path('item/', ItemViewAll.as_view(), name='item_process'),
]

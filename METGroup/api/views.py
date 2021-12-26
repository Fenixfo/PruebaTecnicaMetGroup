import json
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework import generics, serializers
from .models import Items, Store
from .serializers import ItemsSerializer, StoreSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
# Create your views here.

#Obtener todos los datos de Store
class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

#Obtener todos los datos de List
class ItemsList(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

#Autenticación de un Usuario
actualUser=''
@api_view(['POST'])
def auth(request):
    try:
        # username = request.POST.get('username')
        username = request.data['username']
        # password = request.POST.get('password')
        password = request.data['password']
    except:
        data = {
            'username':'This field is required.',
            'password':'This field is required.'
        }
        return JsonResponse(data)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response('Invalid username')

    pwd_valid = check_password(password, user.password)
    if not pwd_valid:
        return Response('Invalid password')

    token, _ = Token.objects.get_or_create(user=user)
    data = {
        'access_token':token.key
    }
    actualUser=username
    return JsonResponse(data)

#Registro de un Usuario
@api_view(['POST'])
def register(request):
    try:
        username = request.data['username']
        password = request.data['password']
    except:
        data = {
            'username':'This field is required.',
            'password':'This field is required.'
        }
        return JsonResponse(data)

    try:
        user = User.objects.get(username=username)
        return Response('Username already exists')
    except User.DoesNotExist:
        if username == '':
            return Response('Invalid username')
        elif password == '':
            return Response('Invalid password')
        else:
            userCreated = User.objects.create(username=username)
            userCreated.set_password(raw_password=password)
            userCreated.save()
    data = {
        'message':'User created succesfully.'
    }
    return JsonResponse(data)

#Store CRUD
class StoreView(View):
    #Políticas de CORS
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Store GET
    def get(self, request, name):
        if name == '':
            return JsonResponse({'message':'Invalid name store'})
        else:
            try:
                store = Store.objects.get(name=name)
                items = Items.objects.filter(storeId=store.id).values()
                data = {
                        'id':store.id,
                        'name':store.name,
                        'items':list(items)
                    }
                return JsonResponse(data)
            except:
                return JsonResponse({'message':'Store name does not exist'})
    #Store POST
    def post(self, request, name):
        if name == '':
            return JsonResponse({'message':'Invalid name store'})
        else:
            try:
                store = Store.objects.get(name=name)
                return JsonResponse({'message':'Name store already exists'})
            except:
                Store.objects.create(name=name)
        store = Store.objects.get(name=name)
        data = {
            'id':store.id,
            'name':store.name,
            'items':[]
        }
        return JsonResponse(data)
    #Store DELETE
    def delete(self, request, name):
        store = list(Store.objects.filter(name=name).values())
        if len(store) > 0:
            Store.objects.filter(name=name).delete()
            return JsonResponse({'message':'Store deleted'})
        else:
            return JsonResponse({'message':'Store name does not exist'})

# Store GET(all)
class StoreViewAll(View):
    #Políticas de CORS
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Store GET(all)
    def get(self, request):
        stores = Store.objects.values()
        for store in stores:
            store['items'] = list(Items.objects.filter(storeId=store['id']).values())
        return JsonResponse({'stores':list(stores)})


#Item CRUD
@api_view(['GET','POST','PUT','DELETE'])
def newItem(request,name):
    #Item POST
    if request.method == 'POST':
        try:
            price = request.data['price']
            storeId_id = request.data['storeId']
        except:
            data = {
                'price':'This field is required.',
                'storeId':'This field is required.'
            }
            return JsonResponse(data)
        if name == '':
            return JsonResponse({'message':'Invalid name item'})
        else:
            try:
                try:
                    store = Store.objects.get(id=storeId_id)
                except:
                    return JsonResponse({'message':'Store id does not exist'})
                item = Items.objects.get(name=name)#, storeId_id=storeId_id)
                return JsonResponse({'message':'Name item already exists'})
            except:
                Items.objects.create(name=name, price=price, storeId_id=storeId_id)
        item = Items.objects.get(name=name, storeId_id=storeId_id)
        data = {
            'id':item.id,
            'name':item.name,
            'price':item.price,
            'storeId':item.storeId_id
        }
        return JsonResponse(data)
    #Item GET
    if request.method == 'GET':
        if name == '':
            return JsonResponse({'message':'Invalid name Item'})
        else:

            try:
                item = Items.objects.filter(name=name).values()[0]
                data = {
                        'id':item['id'],
                        'name':item['name'],
                        'price':item['price'],
                        'store_id':item['storeId_id']
                    }
                return JsonResponse(data)
            except:
                return JsonResponse({'message':'Item name does not exist'})
    #Item PUT
    if request.method == 'PUT':

        try:
            price = request.data['price']
            storeId_id = request.data['storeId']
        except:
            data = {
                'price':'This field is required.',
                'storeId':'This field is required.'
            }
            return JsonResponse(data)
        if price == '':
            return JsonResponse({'message':'Invalid price item'})
        else:
            try:
                store = Store.objects.get(id=storeId_id)
            except:
                return JsonResponse({'message':'Store id does not exist'})
        try:
            item = Items.objects.get(name=name)
            item.price = price
            item.storeId_id = storeId_id
            item.save()
            data = {
                'id':item.id,
                'name':item.name,
                'price':item.price,
                'storeId':item.storeId_id
            }
        except:
            data = {'message':'Item not found'}
        return JsonResponse(data)
    #Item DELETE
    if request.method == 'DELETE':
        item = list(Items.objects.filter(name=name).values())
        if len(item) > 0:
            Items.objects.filter(name=name).delete()
            return JsonResponse({'message':'Item deleted'})
        else:
            return JsonResponse({'message':'Item name does not exist'})

# Store GET(all)
class ItemViewAll(View):
    #Políticas de CORS
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Item GET(all)
    def get(self, request):
        items = Items.objects.values()
        return JsonResponse({'items':list(items)})


import json
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework import generics, serializers
from .models import Items, Store
from .serializers import ItemsSerializer, StoreSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
# Create your views here.

class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ItemsList(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

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
    return JsonResponse(data)

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


class StoreView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    # def put(self, request, name):
    #     jsonData = json.loads(request.body)
    #     stores = list(Store.objects.filter(name=name).values())
    #     if len(stores) > 0:
    #         store = Store.objects.get(name=name)
    #         store.

    def delete(self, request, name):
        store = list(Store.objects.filter(name=name).values())
        if len(store) > 0:
            Store.objects.filter(name=name).delete()
            return JsonResponse({'message':'Store deleted'})
        else:
            return JsonResponse({'message':'Store name does not exist'})
        

class StoreViewAll(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        stores = Store.objects.values()
        for store in stores:
            store['items'] = list(Items.objects.filter(storeId=store['id']).values())
            print(store)
        print(list(stores))
        return JsonResponse({'stores':list(stores)})


class ItemView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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


# A continuación se muestra una forma diferente de obtener y enviar datos

# @api_view(['POST'])
# def newStore(request, name):
# def post(self, request, name):
#     if name == '':
#         return Response('Invalid name store')
#     else:
#         try:
#             store = Store.objects.get(name=name)
#             return Response('Name store already exists')
#         except:
#             Store.objects.create(name=name)
#     store = Store.objects.get(name=name)
#     data = {
#         'id':store.id,
#         'name':store.name,
#         'items':[]
#     }
#     return JsonResponse(data)


# @api_view(['GET'])
# def newStore(request, name):
# def get(self, request, name):
#     if name == '':
#         return Response('Invalid name store')
#     else:
#         try:
#             store = Store.objects.get(name=name)
#             items = Items.objects.filter(storeId=store.id).values()
#             data = {
#                     'id':store.id,
#                     'name':store.name,
#                     'items':list(items)
#                 }
#             return JsonResponse(data)
#         except:
#             return Response('Store name does not exist')

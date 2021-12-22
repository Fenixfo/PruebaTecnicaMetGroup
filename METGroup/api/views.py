from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, serializers
from .models import Store
from .serializers import StoreSerializer

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
        if password == '':
            return Response('Invalid password')
        else:
            userCreated = User.objects.create(username=username)
            userCreated.set_password(raw_password=password)
            userCreated.save()
    data = {
        'message':'User created succesfully.'
    }
    return JsonResponse(data)
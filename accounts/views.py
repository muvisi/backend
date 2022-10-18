from django.shortcuts import render

# Create your views here.
import dataclasses
from datetime import datetime
from django.shortcuts import render
from accounts.serializer import LoginSerializer, UserLoginSerializer
from rest_framework import permissions
from rest_framework.views import APIView
# from accounts.sms import SMS

# from appointment.number_generator import random_string
# from appointment.sms import SMS
# from appointment.util import convert_phone
from .models import AccountModel
from django.shortcuts import get_object_or_404

# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_400_BAD_REQUEST
# from .serializers import *
# from django.utils import timezone
# import pytz


# timezone.activate(pytz.timezone("Africa/Nairobi"))
# timezone.localtime(timezone.now())
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser,MultiPartParser ))
def login(request):
    data = request.data
    
    print(data)
    serializer = LoginSerializer(data=data, context={'request': request})
    if not serializer.is_valid():
        return Response({'error': 'blank username or password'}, status=401)
    user = get_object_or_404(AccountModel,email=serializer.validated_data['email'])
    if not user.check_password(serializer.validated_data['password']):
        return Response({'error': 'Incorrect username or password'}, status=401)
    serializer = UserLoginSerializer(user)
   
    data = serializer.data
    print(data)
    login_time=datetime.now()
    print("USEREMAIL",user.email)
    print("LOGINTIME",login_time)
    obj=AccountModel.objects.get(email=user.email)
    
    obj.last_login==login_time
    obj.save()
    return Response(data)
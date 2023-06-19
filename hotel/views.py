from django.shortcuts import render

# Create your views here.
import dataclasses
from datetime import datetime, timedelta
from django.shortcuts import render
from accounts.models import AccountModel
from hotel.models import Rooms, RoomsBooking
from hotel.serializer import RoomBookingSerializer, RoomSerializers
from rest_framework import permissions
from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication,Token
from django.shortcuts import get_object_or_404

from dateutil.parser import *
from rest_framework import status, viewsets
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_400_BAD_REQUEST

class RoomsSetup(ModelViewSet):
    queryset=Rooms.objects.all()
    serializer_class=RoomSerializers
    
    def create(self,request):
        data=request.data
        newrooms=Rooms.objects.create(
           
            room_block = data['room_block'],
            room_number = data['room_number'],
            room_package= data['room_package'],
            room_price = data['room_price'],            
            # boarding_package = data['boarding_package']                    
           
        ) 
        return Response("OK")
@api_view(['POST'])
@permission_classes((AllowAny,))

@parser_classes((JSONParser,FormParser, ))
def Hotel_Setup(request):
    data = request.data
    user=request.user
    print(user)
    print(data)

    newrooms=Rooms.objects.create(
           
            room_block = data['room_block'],
            room_number = data['room_number'],
            room_package= data['room_package'],
            room_price = data['room_price'],            
            # boarding_package = data['boarding_package']                    
           
        )
    return Response('ok')




@api_view(['GET'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def SetUprooms(request):
    data = request.data
    print(data)
    queryset=Rooms.objects.all()
    serializer=RoomSerializers(queryset,many=True).data

    return Response (serializer)
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def BookRoom(request):
    data = request.data
    print(data)
    # date=((parse(data['date']))+timedelta(days=1)).date()
    book_room=Rooms.objects.get(id=data['id'])
    created=RoomsBooking.objects.create(
                    room=book_room,
                    # booking_date=date,
                    # time=parse(data['time']),
                     names=data['Patient_names'],
                     email=data['Patient_email'],
                     phone=data['Patient_phone'],
                     age=data['Patient_age'],
                     gender=data['Patient_gender'],
                     status="BOOKED"
                
             )
    book_room.status="BOOKED"
    book_room.save()

    return Response ('ok')
@api_view(['GET'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def BookedRooms(request):
    data = request.data
    print(data)
    queryset=RoomsBooking.objects.filter(status="BOOKED").order_by("-created")
    serializer=RoomBookingSerializer(queryset,many=True).data

    return Response (serializer)

@api_view(['GET'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def BookedRoomsReport(request):
    data = request.data
    print(data)
    queryset=RoomsBooking.objects.all().order_by("-created")
    serializer=RoomBookingSerializer(queryset,many=True).data

    return Response (serializer)



@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def Free_Rooms(request):
    data = request.data
    print(data)
    free_room=Rooms.objects.get(id=data['room_id'])
    free_room.status="FREE"
    free_room.save()
    free_booking=RoomsBooking.objects.get(id=data['booking_id'])
    free_booking.status="FREE"
    free_booking.save()

    return Response("ok")

@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def RegisterPatient(request):
    data = request.data
    # check=AccountModel.objects.filter(email=data['email']).count()
    if AccountModel.objects.filter(email=data['email']).count()==0:
        created=AccountModel.objects.create(
                    email=data['email'],
                    role="admin" if data['role']=="Hotel Staff" else "client",

                    
                   
                
             )
        created.set_password(data['password1'])
        created.save()
    

        return Response ("OK")
    else: return Response("User already exist",status=HTTP_400_BAD_REQUEST)



from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword


def getAccessToken(request):
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def lipa_na_mpesa_online(request):
    data=request.data
    phone=data['phone']
    amount=data['amount']
   
    print(data)
   
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount":amount,
        "PartyA": phone,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "sameta hotel Lodge",
        "TransactionDesc": "hotel payments"
    }
    print(request)

    response = requests.post(api_url, json=request, headers=headers)
    
    return Response('success')
@api_view(['POST'])
@permission_classes((AllowAny,))

@parser_classes((JSONParser,FormParser, ))
def Edit_rooms(request):
    data = request.data
    print(data)
    room_created=Rooms.objects.get(id=data['id'])
    room_created.room_block=data['room_block']
    room_created.room_number=data['room_number']
    room_created.room_price=data['room_price']
    room_created.room_package=data['room_package']
    room_created.save()
    return Response("ok")
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((JSONParser,FormParser, ))
def DeleteRoom(request):
    data = request.data
    print(data)
    deletion=Rooms.objects.get(id=data['id'])
    deletion.delete()
    print(deletion)
    return Response("ok")
class ChangePasswordAPIView(APIView):
    parser_classes=(JSONParser,FormParser,MultiPartParser)
    permission_classes=[AllowAny]
    def post(self,request):
        data = request.data
        user=request.user
        if not user.check_password(data['current']):
            return Response("Wrong password",status=HTTP_400_BAD_REQUEST)
        if  data['password1']==data['password2']:
            user.set_password(data['password1'])
            user.save()
            return Response(status=HTTP_200_OK)
        return Response("Passwords does not match",status=HTTP_400_BAD_REQUEST)
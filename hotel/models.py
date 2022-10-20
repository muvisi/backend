from django.db import models

import uuid
from datetime import datetime
from django.conf import settings

User = settings.AUTH_USER_MODEL

from accounts.models import AccountModel




class Rooms(models.Model):
    FREE= "FREE" #NEWLY  CREATED ROOMS DEFAULT FOR ALL
    BOOKED = "BOOKED" #BOOKED ROOMS
    RESERVED = "RESERVED"#VIP BOOKED ROOMS
    MANTAINANCE="MENTAINACE"#ROOMS UNDER MAINTENANCE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room_block=  models.CharField(max_length=200, blank=True, null=True)
    room_number= models.CharField(max_length=200, blank=True, null=True,unique=True)
    room_package= models.CharField(max_length=200, blank=True, null=True)
    room_price= models.CharField(max_length=200, blank=True, null=True)
    boarding_package= models.CharField(max_length=200, blank=True, null=True)
    created =   models.DateTimeField(auto_now_add=True)
    status=models.CharField(default="FREE", max_length=200, blank=True, null=True)



class RoomsBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    # user=models.ForeignKey(AccountModel,on_delete=models.CASCADE)
    status=models.CharField(max_length=200, blank=True, null=True)
    names=  models.CharField(max_length=200, blank=True, null=True)
    email=  models.CharField(max_length=200, blank=True, null=True)
    phone= models.CharField(max_length=200, blank=True, null=True)
    gender=  models.CharField(max_length=200, blank=True, null=True)
    booking_date= models.DateField(blank=True, null=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)
    age= models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return  self.first_name
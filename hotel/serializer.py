from curses import meta
from dataclasses import field, fields
from re import A
from hotel.models import Rooms, RoomsBooking
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers



class RoomSerializers(ModelSerializer):

    class Meta:
        model=Rooms
        fields='__all__' 
class RoomBookingSerializer(ModelSerializer):
    room=RoomSerializers()

    class Meta:
        model=RoomsBooking
        fields='__all__' 
# from django.db import router
from django.urls import path,include
import hotel.views as View

# from rest_framework import routers
name = 'hotel'

from .views import *
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'set-up-roomss',View.RoomsSetup)


urlpatterns = [
        path('set-up-rooms/',View.Hotel_Setup),
        
        path('setuprooms/',View.SetUprooms), 
        path('book-room/',View.BookRoom), 
        path('booked-rooms/',View.BookedRooms),
        path('booked-rooms-report/',View.BookedRoomsReport),
        path('free-rooms/',View.Free_Rooms), 
        path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
        path('online/lipa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
        path('register-patient/',View.RegisterPatient),

        path('edit-rooms/',View.Edit_rooms),
        path('delete-room/',View.DeleteRoom),
        path('change_password/',ChangePasswordAPIView.as_view()),

        path('',include(router.urls)), 
       
]
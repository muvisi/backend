from django.urls import path,include

from rest_framework import routers

from .views import *
from . import views
from rest_framework.routers import DefaultRouter
rs=DefaultRouter()
# rs.register(r'create-user',AccountViewset)
# rs.register(r'staffs',Queryusers)
# rs.register(r'archived',QueryArchivedusers)

# rs.register(r'accounts',AccountViewset)
urlpatterns = [
        path('login/',login), 
      
      


        path('',include(rs.urls)), 
       
]

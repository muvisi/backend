from curses import meta
from dataclasses import field, fields
from re import A
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import AccountModel

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField()



class UserSerializer(ModelSerializer):
	class Meta:
		model=AccountModel
		fields=('id','email','first_name','last_name','last_login','gender','date_joined','is_active','is_staff','is_archive','department','role','phone','deleted_by','deleted_date')
class AccountSerializer(ModelSerializer):
	token = serializers.SerializerMethodField()
	class Meta:
		model=AccountModel
		fields=('email','first_name','last_name','gender','date_joined','is_active','is_staff','token','department','role','phone')
    
class UserLoginSerializer(AccountSerializer):
    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token
class WhatappLoginSerializer(ModelSerializer):
	token=SerializerMethodField()
	class Meta:
		model=AccountModel
		fields=('role','token')

	def get_token(self, obj):
		payload = jwt_payload_handler(obj)
		token = jwt_encode_handler(payload)
		return token


class UsersDownloadSerializer(ModelSerializer):
	class Meta:
	
		model=AccountModel
		fields=('email','first_name','last_name','phone','department','date_joined')
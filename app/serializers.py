from dataclasses import fields
from rest_framework import serializers
from .models import User,Profile,Comment,Module,Session,Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

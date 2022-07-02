from dataclasses import fields
from importlib.metadata import files
from rest_framework import serializers
from .models import User,Profile,Comment,Module,Session,Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Module(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)

    class Meta:
        model = Module
        fields = '__all__'







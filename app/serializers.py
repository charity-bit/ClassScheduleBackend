from rest_framework import serializers
from .models import User,Profile,Comment,Module,Session,Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    class Meta:
        model = Module
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True) 
    modules = ModuleSerializer(read_only =True )
    class Meta:
        model = Profile
        fields = '__all__'







from rest_framework import serializers
from .models import User, Profile, Comment, Module, Session, Announcement
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)

    class Meta:
        model = Module
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modules = ModuleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'



class SessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True) 
    module = ModuleSerializer(read_only =True )
    class Meta:
        model=Session
        fields='__all__'



class AnnouncementSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True) 
    class Meta:
        model=Announcement
        fields='__all__'



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True) 
    class Meta:
        model=Comment
        fields='__all__'
        
        
    


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modules = ModuleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        # read_only_fields=['user','modules']


class loginSerializer(serializers.Serializer):
    email=serializers.CharField(write_only=True,required=True)
    password=serializers.CharField(write_only=True,required=True)

    def validate_user(self):
        new_user=authenticate(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )
        if new_user is not None:
            return new_user
        raise serializers.ValidationError('The User does not Exist')
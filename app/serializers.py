from rest_framework import serializers
from .models import User, Profile, Comment, Module, Session, Announcement
from django.contrib.auth import authenticate
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Module
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modules = ModuleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = '__all__'
        
    # create_comment=Comment.objects.create()
class SessionSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)
    module = ModuleSerializer(read_only=True)
    module_id = serializers.IntegerField(write_only = True)
    # session_comments = CommentSerializer(read_only = True)
    no_hours = serializers.IntegerField(read_only =True)

    class Meta:
        model = Session
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    technical_mentor = UserSerializer(read_only=True)
    technical_mentor_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = Announcement
        fields = "__all__"

   





class UpdateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    modules = ModuleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        # read_only_fields=['user','modules']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)


    
    def validate_user(self):
        email = self.validated_data["email"]
        regex = "@([a-z\S]+)"
        result = re.split(regex, email)
        # Check if the emails are from moringa
        if result[1] == "student.moringaschool.com" or result[1] == "moringaschool.com":
            new_user = authenticate(
                email=self.validated_data["email"],
                password=self.validated_data["password"],
            )
            if new_user is not None:
                return new_user
            raise serializers.ValidationError("The User does not Exist")

        raise serializers.ValidationError('Invalid Email ')


# User create serializer
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = self.validated_data["email"]
        regex = "@([a-z\S]+)"
        result = re.split(regex, email)
        # Check if the emails are from moringa
        if result[1] == "student.moringaschool.com" or result[1] == "moringaschool.com":
            user = User.objects.create_user(**validated_data)
            
            return user

        serializers.ValidationError('Invalid Email')
        

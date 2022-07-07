import profile
from django.http import HttpResponse, JsonResponse
import re

# from django.shortcuts import render
from rest_framework.decorators import api_view
from app import serializers
from app.serializers import (
    AnnouncementSerializer,
    UserCreateSerializer,
    UserSerializer,
    ModuleSerializer,
    CreateModuleSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    SessionSerializer,
    CommentSerializer,
    LoginSerializer,
)
from .permissions import ModulePermissions

from rest_framework.response import Response
from app.models import User, Module, Profile, Session, Announcement, Comment
from rest_framework import status, generics
from django.http import Http404

# from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.schemas import get_schema_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

# from .permissions import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def api(request):
    return HttpResponse("this is the backed for classroom schedule")


# login user api
class LoginAPIView(APIView):
    """

    Login User APIView

    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validate_user()
            data = {
                "message": "User logged in successfully",
                "email": user.email,
                "user_type": user.user_type,
            }

            # get auth token
            token, created = Token.objects.get_or_create(user=user)
            data["token"] = token.key

            responseStatus = status.HTTP_200_OK

            return Response(data, status=responseStatus)

        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create user api
class UserCreateAPIView(APIView):
    """

    Create User API

    """

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, format=None):
        data = request.data
        email = data["email"]

        regex = "@([a-z\S]+)"
        result = re.split(regex, email)
        if result[1] == "student.moringaschool.com":
            user_type = "STUD"
        elif result[1] == "moringaschool.com":
            user_type = "TM"

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type=user_type)
            data = {"email": data["email"], "message": "User created successfully"}

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# logout user apiview


class LogoutAPIView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# Adding comments
@api_view(["POST"])
def create_comment(request, format=None):
    serializers = CommentSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# getting all comments posted
@api_view(["GET"])
def all_comments(request, format=None):
    comments = Comment.objects.all()
    serializers = CommentSerializer(comments, many=True)
    return Response(serializers.data)


# Getting all announcements made by the TM
@api_view(["GET"])
def all_announcements(request, format=None):
    announcements = Announcement.objects.all()
    serializers = AnnouncementSerializer(announcements, many=True)
    return Response(serializers.data)


# Getting the sessions and the details
@api_view(["GET"])
def get_session_details(request, format=None):
    session_details = Session.objects.all()
    serializers = SessionSerializer(session_details, many=True)
    return Response(serializers.data)


# Getting the available sessions
@api_view(["GET"])
def get_available_session(request, session_id):
    available_session = Session.objects.filter(id=session_id).first()
    serializers = SessionSerializer(available_session, many=True)
    return Response(serializers.data)


# Updating the student Profile
class studentprofileupdateAPIview(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    serializer_class = UpdateProfileSerializer
    parser_class = (
        MultiPartParser,
        FormParser,
    )

    def get_profile(self):

        email = self.kwargs["email"]
        new_obj = get_object_or_404(User, email=email)
        return new_obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ModuleViewSet(viewsets.ModelViewSet):
    permission_classes = [ModulePermissions]
    serializer_class = CreateModuleSerializer
    queryset = Module.objects.all()


@api_view(["POST"])
def add_student(request,module_id,student_id):
    user = User.objects.get(id = student_id)
    if user.user_type == 'STUD':
        profile = Profile.objects.get(user = user)
        module = Module.objects.get(id = module_id)
        if module in profile.modules.all():
            return Response({"message":"This user is already inrolled in the module"})

        else:
            profile.modules.add(module)
            return Response({"messsage":"module added successfully"})
    else:
        return Response({
            "message":'This user is not a student'
        })

# get sessions for a specific module
@api_view(["GET"])
def get_module_sessions(request,module_id):
   
    module = Module.objects.get(id = module_id)
    sessions = Session.objects.filter(module = module).all()
    serializers = SessionSerializer(sessions, many=True)
    return Response(serializers.data)

# get students modules
@api_view(['GET'])
def get_student_modules(request,student_id):
    # user_id=request.data['user']
    user = User.objects.get(id = student_id)
    if user.user_type == 'STUD':
        profile = Profile.objects.get(user = user)
        modules = profile.modules.all()
        serializers = ModuleSerializer(modules,many=True)
        return Response(serializers.data)

    else:
        return Response({"message":"The user is not a student"})




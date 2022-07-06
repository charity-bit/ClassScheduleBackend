from django.http import HttpResponse, JsonResponse
import re
from requests import request

# from django.shortcuts import render
from rest_framework.decorators import api_view
from app.serializers import (
    AnnouncementSerializer,
    UserCreateSerializer,
    UserSerializer,
    ModuleSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    SessionSerializer,
    CommentSerializer,
    LoginSerializer,
    AnnouncementCommentSerializer,
    ChangePasswordSerializer,
)
from .permissions import TMPermissions

from rest_framework.response import Response
from app.models import User, Module, Profile, Session, Announcement, Comment,AnnounComment
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
from django.db.models import Q 
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
            # data["User"]=user

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


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer




# creating comments using viewset
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related("session","student").all()
   


class AnnouncementCommentViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnounComment.objects.select_related("student","announcement").all()

# @api_view(["POST"])
# def LikesView(request, comment_id):
#     current_user = request.user
#     user = User.objects.get(email=current_user.email)
#     user_id=User.objects.get(id=user.id)
#     # user_id = User.objects.get(id=9)
    
#     # post_id = Post.objects.get(pk=pk)
#     try:
#         comment_id = Comment.objects.get(comment_id=comment_id)
#     except Comment.DoesNotExist:
#         comment_id= None
#     # get_object_or_404(Likes, pk=post_id)
#     check = Likes.objects.filter(Q(user_id=user_id) and Q(comment_id=comment_id))
#     # check=Likes.object.get_object_or_404(Likes, pk=comment_id)
#     if(check.exists()):
#         return Response({
#             "status": status.HTTP_400_BAD_REQUEST,
#             "message": "You only like once"
#         })
#     new_like = Likes.objects.create(user_id=user_id, comment_id=comment_id)
#     new_like.save()
#     serializer = LikesSerializer(new_like)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)



# Getting all announcements made by the TM
@api_view(["GET"])
def all_announcements(request, format=None):
    announcements = Announcement.objects.all()
    serializers = AnnouncementSerializer(announcements, many=True)
    return Response(serializers.data)


# Getting the sessions and the details
@api_view(["GET"])
def get_session_details(request,session_id):
    session_details = Session.objects.filter(id=session_id).first()
    serializers = SessionSerializer(session_details, many=False)
    return Response(serializers.data)


# Getting the available sessions
@api_view(["GET"])
def get_available_session(request, session_query):
    available_sessions = Session.objects.filter(title__icontains=session_query)
    serializer = SessionSerializer(available_sessions, many=True)
    return Response(serializer.data)


# Updating the student Profile
class StudentProfileUpdateAPIview(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    lookup_field = 'email'
    queryset = Profile.objects.all()
  
    def put(self, request, *args, **kwargs):
        serializer = UpdateProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ModuleViewSet(viewsets.ModelViewSet):
    # uncomment permissions later
    # permission_classes = [TMPermissions]
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

   
class AnnouncementViewSet(viewsets.ModelViewSet):
    # permission_classes = [TMPermissions]
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()


class SessionViewSet(viewsets.ModelViewSet):
    # permission_classes = [TMPermissions]
    serializer_class = SessionSerializer
    queryset = Session.objects.select_related("module","technical_mentor")



       
       



  
  

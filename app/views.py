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
                "user_id":user.id
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
        print("data",data)
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
    queryset = Comment.objects.select_related("session","user").all()
   



class AnnouncementCommentViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementCommentSerializer
    queryset = AnnounComment.objects.select_related("student","announcement").all()




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



@api_view(['GET'])
def get_profile(request,user_id):
    user = User.objects.get(id = user_id)
    if user:
        profile = Profile.objects.filter(user = user).first()
        serializers = UpdateProfileSerializer(profile)
        return Response(serializers.data)

# class ProfileAPIview(generics.GenericAPIView):
#     # lookup_field = 'user'
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

#     def get(self, request, pk=None):
#         instance = self.get_object()
#         print("instance",instance)
#         # instance.bio=request.data['bio']
#         # instance.profile_image=request.data['profile_image']
#         # instance.get_fields=['bio','profile_image']
#         serializer = ProfileSerializer(instance)
#         return Response(serializer.data)



class ProfileUpdateAPIview(generics.GenericAPIView):
    # lookup_field = 'user'
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer


    def put(self, request, pk=None):
        instance = self.get_object()
        print("instance",instance)
        instance.bio=request.data['bio']
        instance.profile_image=request.data['profile_image']
        # instance.active = False
        instance.save(update_fields=['bio','profile_image'])
        return Response('done')



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




  # get modules by a certain TM
@api_view(['GET'])
def get_tm_modules(request,tm_id):
    user = User.objects.get(id = tm_id)
    # fix check if there is a user
    
    if user.user_type == 'TM':
        modules = Module.objects.filter(technical_mentor = user).all()
        serializers = ModuleSerializer(modules,many=True)
        return Response(serializers.data)
            
    else:
        # if the user is not a tm
        return Response({"message":"The user is not a Technical_mentor"})

 

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


@api_view(['GET'])
def technical_mentors(request):
    technical_mentors = User.objects.filter(user_type = 'TM').all()
    serializers = UserSerializer(technical_mentors,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def students(request):
    students = User.objects.filter(user_type = 'STUD').all()
    serializers = UserSerializer(students,many=True)
    return Response(serializers.data)


@api_view(["POST"])
def like_comment(request,comment_id):
    user_id=request.data['user']
    user=User.objects.filter(pk=user_id).first()
    comment=Comment.objects.filter(pk=comment_id).first()
    if user is None:
        return Response({
            "message":"Authentication required"
        })
    
    if comment is not None:
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({
            "message":"like removed"
        })
        else:
            comment.likes.add(user)
            return Response({
            "message":"like added"
        })
    else:
        return Response({
            "message":"comment not found"
        })

  
@api_view(["POST"])
def like_announ_comment(request,announcomment_id):
    user_id=request.data['user']
    user=User.objects.filter(pk=user_id).first()
    announcomment=AnnounComment.objects.filter(pk=announcomment_id).first()
    if user is None:
        return Response({
            "message":"Authentication required"
        })
    
    if announcomment is not None:
        if user in announcomment.likes.all():
            announcomment.likes.remove(user)
            return Response({
            "message":"like removed"
        })
        else:
            announcomment.likes.add(user)
            return Response({
            "message":"like added"
        })
    else:
        return Response({
            "message":"comment not found"
        })

@api_view(['GET'])
def get_session_comments(request,session_id):
    session = Session.objects.get(id = session_id)
    if session:
        comments = Comment.objects.filter(session = session).all()
        serializers = CommentSerializer(comments,many = True)
        return Response(serializers.data)


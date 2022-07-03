from django.http import HttpResponse, JsonResponse
from requests import request
# from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import AnnouncementSerializer, UserSerializer,ModuleSerializer,ProfileSerializer,UpdateProfileSerializer,SessionSerializer,CommentSerializer
from rest_framework.response import Response
from app.models import User,Module,Profile,Session,Announcement,Comment
from rest_framework import status,generics
from django.http  import Http404
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
# from rest_framework.schemas import get_schema_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
from .permissions import *
from rest_framework.authtoken.models import Token
# Create your views here.

def api(request):
    return HttpResponse('this is the backed for classroom schedule')




@api_view(['POST']) 
def create_comment(request,format=None):
    serializers=CommentSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def all_comments(request,format=None):
    comments=Comment.objects.all()
    serializers=CommentSerializer(comments,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def all_announcements(request,format=None):
    announcements=Announcement.objects.all()
    serializers=AnnouncementSerializer(announcements,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def get_session_details(request,format=None):
    session_details=Session.objects.all()
    serializers=SessionSerializer(session_details,many=True)
    return Response(serializers.data)

@api_view(['GET'])
def get_available_session(request,session_id):
    available_session=Session.objects.filter(id=session_id).first()
    serializers=SessionSerializer(available_session,many=True)
    return Response(serializers.data)

class studentprofileupdateAPIview(generics.RetrieveAPIView,
                                   mixins.UpdateModelMixin):
    serializer_class = UpdateProfileSerializer
    parser_classes = (MultiPartParser, FormParser,)

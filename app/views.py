from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

def api(request):
    return HttpResponse('this is the backed for classroom schedule')
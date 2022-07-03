from django.urls import path
from app import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Schedule API",
      default_version='v1',
      description="Test description",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/',views.api,name='api'),
   path('api/apis/creatercomment/', views.create_comment,name=''),
   path('api/allcomments/', views.all_comments,name=''),
   path('api/allannouncement/', views.all_announcements,name=''),
   path('api/sessiondetails/', views.get_session_details,name=''),
   
]

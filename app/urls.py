from django.urls import path

from app import views
from app.views import ModuleViewSet,CommentViewSet

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

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


router = DefaultRouter()

router.register(r'modules',ModuleViewSet),
router.register(r'comments',CommentViewSet)


urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/',views.api,name='api'),
   
   # comments
   # path('api/comments/create/', views.create_comment,name=''),
   # path('api/comments/', views.all_comments,name=''),

   # Likes
   # path('api/likes/<comment_id>', views.LikesView,name=''),

   # announcements
   path('api/announcements/', views.all_announcements,name=''),

   # sessions
   path('api/sessions/detail/<session_id>', views.get_session_details,name=''),
   path('api/sessions/search/<session_id>', views.get_available_session,name=''),
   # Updating Student Profile
   path('api/student/profile/update/',views.StudentProfileUpdateAPIview.as_view(),name=''),
   # Create user api
   path('api/user/create/',views.UserCreateAPIView.as_view(),name=''),
   path('api/user/login/',views.LoginAPIView.as_view(),name=''),
   path('api/user/logout/',views.LogoutAPIView.as_view(),name='')


   

] + router.urls

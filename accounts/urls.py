from django.urls import include, path
from django.conf.urls import url
from knox import views as knox_views
from .api import UserAPI, RegisterAPI, LoginAPI, ProfileViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, 'profile')

# The method handlers for a ViewSet are only bound to the corresponding actions at the point of finalizing the view, 
# using the .as_view() method.

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    url(r'^api/', include(router.urls))
]

from django.urls import include, path
from knox import views as knox_views
from .api import UserAPI, RegisterAPI, LoginAPI

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]
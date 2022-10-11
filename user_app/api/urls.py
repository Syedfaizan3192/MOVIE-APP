from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api.views import registration, logout_view

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration, name='register'),
    path('logout/', logout_view, name='logout'),
]

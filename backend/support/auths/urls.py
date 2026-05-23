from rest_framework.authtoken import views
from django.urls import path, include


urlpatterns = [
    path('login', views.obtain_auth_token, name='api-token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
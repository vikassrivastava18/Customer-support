from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView,
                                   SpectacularRedocView)
from .views import CustomAuthToken


urlpatterns = [
    path('admin/', admin.site.urls),
    # Schema Generation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc UI
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('login', CustomAuthToken.as_view(), name='api-token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('staff/', include('staff.urls')),
    path('', include('author.urls')),
]

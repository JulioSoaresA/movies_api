from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from movie.views import FilmeViewSet
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.permissions import AllowAny

schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Movies API',
        default_version='1.0.0',
        description='API documentation of Movies',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
router.register('filmes', FilmeViewSet, basename='Filmes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('usuario/', include('users.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
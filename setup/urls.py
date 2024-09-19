from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from movie.views import FilmeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('filmes', FilmeViewSet, basename='Filmes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
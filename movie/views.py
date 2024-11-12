from movie.models import Filme
from rest_framework import viewsets, filters
from rest_framework.permissions import DjangoModelPermissions
from .serializers import FilmeSerializer
from django_filters.rest_framework import DjangoFilterBackend



class FilmeViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Filme.objects.all().order_by('id')
    serializer_class = FilmeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['titulo', 'ano_lancamento', 'avaliacao_media']
    search_fields = ['titulo', 'genero', 'ano_lancamento']

from django.contrib import admin
from movie.models import Filme

class FilmeAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'ano_lancamento', 'genero', 'classificacao_etaria', 'avaliacao_media')
    list_display_links = ('id', 'titulo')
    search_fields = ('titulo', 'genero', 'ano_lancamento', 'genero')
    list_filter = ('genero', 'classificacao_etaria')
    list_per_page = 20


admin.site.register(Filme, FilmeAdmin)

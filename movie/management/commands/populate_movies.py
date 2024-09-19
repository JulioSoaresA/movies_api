import requests
from django.core.management.base import BaseCommand
from ...models import Filme
from datetime import timedelta
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os

# Substitua pela sua chave de API da TMDb
API_KEY = '8daf33bd13563661f23bd756dfb3e3dd'
MOVIE_API_URL = f"https://api.themoviedb.org/3/movie/popular?language=en&api_key={API_KEY}&page={{page}}"
GENRE_API_URL = f"https://api.themoviedb.org/3/genre/movie/list?language=en&api_key={API_KEY}"
MOVIE_DETAILS_URL = f"https://api.themoviedb.org/3/movie/{{movie_id}}?language=en-US&api_key={API_KEY}"

class Command(BaseCommand):
    help = 'Popula o banco de dados com filmes da API de filmes'

    def get_genres(self):
        """Busca a lista de gêneros e retorna um dicionário mapeando id para nome."""
        response = requests.get(GENRE_API_URL)
        if response.status_code == 200:
            genres = response.json().get('genres', [])
            return {genre['id']: genre['name'] for genre in genres}  # {id: nome}
        else:
            self.stdout.write(self.style.ERROR('Erro ao buscar gêneros: {}'.format(response.status_code)))
            return {}

    def get_movie_details(self, movie_id):
        """Busca os detalhes de um filme, incluindo sua duração."""
        response = requests.get(MOVIE_DETAILS_URL.format(movie_id=movie_id))
        if response.status_code == 200:
            return response.json()
        else:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar detalhes do filme {movie_id}: {response.status_code}'))
            return {}
    
    def download_image(self, url, filename):
        """Baixa a imagem da URL e salva localmente no diretório de mídia."""
        response = requests.get(url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            return File(img_temp, name=filename)
        else:
            self.stdout.write(self.style.ERROR(f'Erro ao baixar a imagem: {url}'))
            return None

    def handle(self, *args, **kwargs):
        # Buscar a lista de gêneros antes de iterar sobre os filmes
        genres = self.get_genres()

        total_filmes = 0
        max_pages = 2  # Defina quantas páginas deseja buscar (cada página tem 20 filmes)

        for page in range(1, max_pages + 1):
            response = requests.get(MOVIE_API_URL.format(page=page))
            if response.status_code == 200:
                filmes = response.json().get('results', [])
                for filme in filmes:
                    # Obter os detalhes completos do filme
                    movie_id = filme['id']
                    detalhes_filme = self.get_movie_details(movie_id)

                    # Extraia os dados desejados da API
                    titulo = filme['title']
                    descricao = filme['overview']
                    ano_lancamento = int(filme['release_date'].split('-')[0]) if filme.get('release_date') else None

                    # Extraia a duração do filme dos detalhes
                    duracao_em_minutos = detalhes_filme.get('runtime', 0)
                    duracao = timedelta(minutes=duracao_em_minutos)

                    # Mapear os genre_ids para os nomes correspondentes
                    genero_ids = filme.get('genre_ids', [])
                    genero = ', '.join([genres.get(genre_id, 'Desconhecido') for genre_id in genero_ids])

                    classificacao_etaria = filme.get('adult', False)
                    idioma_original = filme.get('original_language', 'en')
                    data_estreia = filme.get('release_date')
                    avaliacao_media = filme.get('vote_average', 0.0)
                    poster_url = filme.get('poster_path', None)

                    # Baixar e salvar a imagem
                    poster_filename = poster_url.split('/')[-1] if poster_url else None
                    poster = self.download_image(f"https://image.tmdb.org/t/p/w500{poster_url}", poster_filename) if poster_url else None

                    # Salvar no banco de dados
                    filme_obj = Filme(
                        titulo=titulo,
                        descricao=descricao,
                        ano_lancamento=ano_lancamento,
                        duracao=duracao,
                        genero=genero,
                        classificacao_etaria="18+" if classificacao_etaria else "Livre",
                        idioma_original=idioma_original,
                        data_estreia=data_estreia,
                        avaliacao_media=avaliacao_media,
                    )

                    if poster:
                        try:
                            filme_obj.poster.save(poster_filename, poster)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Erro ao salvar o poster: {e}'))

                    # Verificar se o filme já existe no banco de dados antes de salvar
                    if not Filme.objects.filter(titulo=titulo, ano_lancamento=ano_lancamento).exists():
                        filme_obj.save()
                    else:
                        self.stdout.write(self.style.WARNING(f'O filme "{titulo}" já existe no banco de dados.'))

                total_filmes += len(filmes)
                self.stdout.write(self.style.SUCCESS(f'Página {page} processada com {len(filmes)} filmes.'))

            else:
                self.stdout.write(self.style.ERROR(f'Erro ao acessar a API na página {page}: {response.status_code}'))
                break

        self.stdout.write(self.style.SUCCESS(f'Banco de dados populado com {total_filmes} filmes!'))

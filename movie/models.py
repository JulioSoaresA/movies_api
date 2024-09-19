from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    ano_lancamento = models.IntegerField()
    duracao = models.DurationField()
    genero = models.CharField(max_length=100)
    classificacao_etaria = models.CharField(max_length=10)
    idioma_original = models.CharField(max_length=100)
    data_estreia = models.DateField()
    avaliacao_media = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.titulo


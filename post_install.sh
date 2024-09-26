#!/bin/bash

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Popular o banco de dados com filmes
python manage.py populate_movies

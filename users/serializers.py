from django.contrib.auth.models import User
from movie.models import Filme
from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remover o campo confirm_password, pois não faz parte do modelo
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        
        # Obter o ContentType para o modelo Filme
        filme_content_type = ContentType.objects.get_for_model(Filme)
        
        # Obter a permissão 'view_filme'
        permission = Permission.objects.get(
            codename='view_filme',
            content_type=filme_content_type
        )
        
        # Atribuir a permissão de visualização do filme ao novo usuário
        user.user_permissions.add(permission)
        
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')

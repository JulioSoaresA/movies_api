from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserSerializer


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            
            request.data['refresh'] = refresh_token
            
            response = super().post(request, *args, **kwargs)
            
            tokens = response.data
            access_token = tokens['access']
            
            res = Response()
            
            res.data = {
                'refreshed': True,
            }
            
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='None',
                path='/'
            )
            
            return res
            
        except:
            return Response({'refreshed': False})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    throttle_classes = [AnonRateThrottle]


class LoginView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle]
    def post(self, request, *args, **kwargs):
        try:
            # Cria uma instância do serializer e valida os dados
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Obtém o usuário autenticado através do serializer
            user = serializer.user

            # Gera os tokens
            tokens = serializer.validated_data

            # Serializa os dados do usuário
            user_serializer = UserSerializer(user)

            # Cria a resposta customizada com tokens e dados do usuário
            res = Response()
            res.data = {
                'success': True,
                'user': user_serializer.data  # Inclui os dados do usuário
            }

            # Configura o cookie do access_token
            res.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                samesite='None',
                secure=True,
                path='/'
            )

            return res

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        
        response = Response({
            'success': 'Logged out successfully'
        })
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=400)

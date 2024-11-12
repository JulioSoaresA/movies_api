from django.urls import path
from .views import LoginView, CustomRefreshTokenView, RegisterView, logout

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
]

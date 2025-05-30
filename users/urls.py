from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register"
    ),
    path(
        "token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]

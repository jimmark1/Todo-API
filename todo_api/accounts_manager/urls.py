from django.urls import path
from . views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('user-details/', RetrieveUserView.as_view(), name='user-details'),

    #SIMPLE JWT AUTHENTICATION
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

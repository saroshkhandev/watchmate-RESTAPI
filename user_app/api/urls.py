from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# this library is to import the json web token views
from user_app.api import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.logout_view, name='logut'),
    path('register/', views.registration_view, name='register'),
    
    # These are the custom urls for jwt(json web token)
    # api/token/ - url takes username and password and generates the access token and refresh token as well
    # access token is required to access the authenticated views [IsAuthenticatedOrReadOnly]
    # access token life is 5 minutes and it expires after that
    # refresh token is to regenerate the new access token for those particular credentials
    # so the url api/token/refresh/ - takes refresh <refresh token code> as input and then gives new access token
    # the life of refresh token is for 24 hours
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Json web tokens are not stored in our database but is stored in the users local storage not in the servers'
    # database
]

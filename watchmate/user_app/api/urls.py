from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token #obtain_auth_token is a built-in view that comes with DRF. It provides an endpoint for users to obtain an authentication token by sending their username and password.
from user_app.api import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView






urlpatterns = [
  path('login/', obtain_auth_token, name='login'), # This URL pattern maps the 'login/' endpoint to the obtain_auth_token view. When a user sends a POST request to this endpoint with their username and password, they will receive an authentication token in response.
  path('register/', views.registration_view, name='register'),                    # -----> This Login,Register,Logout API is used for Token Authentication.  
  path('logout/', views.logout_view, name='logout'),
  
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    #------> This URL Pattern is used for JWT Authentication 
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
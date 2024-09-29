

from django.urls import path
from user_authentication import views

urlpatterns = [
    path('', views.login_view, name='login'),  #by default view 127.0.0.1:8000
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
]


from django.urls import path
from user_authentication import views
from .views import UserListView,AddUserView,DeleteUserView

urlpatterns = [
    path('', views.login_view, name='login'),  #by default view 127.0.0.1:8000
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('signout/', views.signout, name='signout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', AddUserView.as_view(), name='user_add'),
    path('users/delete/<int:user_id>/', DeleteUserView.as_view(), name='user_delete'),
]
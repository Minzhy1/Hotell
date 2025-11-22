from django.urls import path
from hotel import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('service/', views.home, name='service'),
    path('clients/', views.clients, name='clients'),
    path('', views.user_logout, name='user_logout'),


]

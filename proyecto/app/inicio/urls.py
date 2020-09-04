
from django.urls import path
from proyecto.app.inicio import views
urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('cerrar-sesion', views.cerrarSesion, name='close'),
    path('getUsers', views.getUsers, name='users'),
    path('registerNewUser', views.registerNewUser, name='register'),
]

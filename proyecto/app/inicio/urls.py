
from django.urls import path
from proyecto.app.inicio import views
urlpatterns = [
    path('', views.index, name='main'),
    path('dashboard', views.dashboard, name='dashboard'),
]

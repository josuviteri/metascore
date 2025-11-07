from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videojuegos/', views.lista_videojuegos, name='videojuegos'),
    path('videojuegos/<int:videojuego_id>/', views.detalle_videojuego, name='detalle_videojuego'),
    path('generos/', views.lista_generos, name='generos'),
    path('generos/<int:genero_id>/', views.detalle_genero, name='detalle_genero'),
    path('plataformas/', views.lista_plataformas, name='plataformas'),
    path('plataformas/<int:plataforma_id>/', views.detalle_plataforma, name='detalle_plataforma'),
    path("formulario/", views.formulario, name="formulario"),
    path("videojuegos/crear/", views.sugerir_videojuego, name="sugerir_videojuego")
]

from django.urls import path
from .views import (
    IndexView, VideojuegoListView, VideojuegoDetailView,
    GeneroListView, GeneroDetailView, PlataformaListView,
    PlataformaDetailView, VideojuegoCreateView, ContactoView
)

urlpatterns = [
    # Nota: Usamos .as_view() al final de cada clase
    path('', IndexView.as_view(), name='index'),
    
    path('videojuegos/', VideojuegoListView.as_view(), name='videojuegos'),
    # Fíjate que cambiamos <int:videojuego_id> por <int:pk>, es el estándar de las clases
    path('videojuegos/<int:pk>/', VideojuegoDetailView.as_view(), name='detalle_videojuego'),
    
    path('generos/', GeneroListView.as_view(), name='generos'),
    path('generos/<int:pk>/', GeneroDetailView.as_view(), name='detalle_genero'),
    
    path('plataformas/', PlataformaListView.as_view(), name='plataformas'),
    path('plataformas/<int:pk>/', PlataformaDetailView.as_view(), name='detalle_plataforma'),
    
    path("formulario/", VideojuegoCreateView.as_view(), name="formulario"),

    path("formulario_contacto/", ContactoView.as_view(), name="formulario_contacto"),


]
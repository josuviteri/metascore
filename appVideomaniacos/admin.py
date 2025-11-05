from django.contrib import admin
from .models import Genero, Plataforma, Videojuego

# Register your models here.

admin.site.register(Genero)
admin.site.register(Plataforma)
admin.site.register(Videojuego)

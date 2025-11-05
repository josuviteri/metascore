from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Genero, Plataforma, Videojuego

# Create your views here.

def index(request):
    generos = Genero.objects.all()
    videojuegos_por_genero = {g: Videojuego.objects.filter(genero=g).order_by('-fecha_lanzamiento').first() for g in generos}
    return render(request, 'index.html', {'videojuegos_por_genero': videojuegos_por_genero})

def lista_videojuegos(request):
    videojuegos = Videojuego.objects.all()
    return render(request, 'videojuegos.html', {'videojuegos': videojuegos})

def detalle_videojuego(request, videojuego_id):
    videojuego = get_object_or_404(Videojuego, pk=videojuego_id)
    return render(request, 'detalle_videojuego.html', {'videojuego': videojuego})

def lista_generos(request):
    generos = Genero.objects.all()
    return render(request, 'generos.html', {'generos': generos})

def detalle_genero(request, genero_id):
    genero = get_object_or_404(Genero, pk=genero_id)
    videojuegos = Videojuego.objects.filter(genero=genero)
    return render(request, 'detalle_genero.html', {'genero': genero, 'videojuegos': videojuegos})

def lista_plataformas(request):
    plataformas = Plataforma.objects.all()
    return render(request, 'plataformas.html', {'plataformas': plataformas})

def detalle_plataforma(request, plataforma_id):
    plataforma = get_object_or_404(Plataforma, pk=plataforma_id)
    videojuegos = plataforma.videojuego_set.all()
    return render(request, 'detalle_plataforma.html', {'plataforma': plataforma, 'videojuegos': videojuegos})

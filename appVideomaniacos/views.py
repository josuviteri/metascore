from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from .models import Genero, Plataforma, Videojuego
import os, re

def _guardar_en_static_images(archivo):
    base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dest_dir = os.path.join(base_dir, 'appVideomaniacos', 'static', 'images')
    os.makedirs(dest_dir, exist_ok=True)

    nombre = os.path.basename(getattr(archivo, 'name', 'imagen.png'))
    nombre = re.sub(r'\s+', '_', nombre)
    nombre = re.sub(r'[^A-Za-z0-9._-]+', '', nombre)

    nombre_sin_ext, ext = os.path.splitext(nombre)
    final_name = nombre
    i = 1
    while os.path.exists(os.path.join(dest_dir, final_name)):
        final_name = f"{nombre_sin_ext}_{i}{ext}"
        i += 1

    dest_path = os.path.join(dest_dir, final_name)
    with open(dest_path, 'wb+') as destino:
        for chunk in archivo.chunks():
            destino.write(chunk)

    return final_name

def index(request):
    generos = Genero.objects.all()
    videojuegos_por_genero = {}
    for genero in generos:
        videojuego = Videojuego.objects.filter(genero=genero).order_by('-fecha_lanzamiento').first()
        videojuegos_por_genero[genero] = videojuego
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

def formulario(request):
    generos = Genero.objects.all().order_by('nombre')
    plataformas = Plataforma.objects.all().order_by('nombre')
    return render(request, 'formulario.html', {'generos': generos, 'plataformas': plataformas})

@transaction.atomic
def sugerir_videojuego(request):
    if request.method != 'POST':
        return redirect('formulario')

    titulo = request.POST.get('titulo', '').strip()
    genero_id = request.POST.get('genero_id')
    plataformas_ids = request.POST.getlist('plataformas_ids')
    fecha_lanzamiento = request.POST.get('fechalanzamiento')
    score = request.POST.get('score')
    descripcion = request.POST.get('descripcion', '').strip()

    imagen_archivo = request.FILES.get('imagen')
    imagen_nombre_input = (request.POST.get('imagen_nombre') or '').strip()

    if not titulo or not genero_id or not plataformas_ids or not fecha_lanzamiento or score is None:
        messages.error(request, 'Completa todos los campos obligatorios.')
        return redirect('formulario')

    genero = get_object_or_404(Genero, pk=genero_id)

    # si se sube archivo, lo copiamos a static/images; si no, usamos el nombre
    if imagen_archivo:
        imagen_final = _guardar_en_static_images(imagen_archivo)
    elif imagen_nombre_input:
        imagen_final = os.path.basename(imagen_nombre_input)
    else:
        imagen_final = 'placeholder.png'

    v = Videojuego(
        titulo=titulo,
        genero=genero,
        descripcion=descripcion,
        fecha_lanzamiento=fecha_lanzamiento,
        score=score,
        imagen=imagen_final,   # solo el nombre en DB
    )
    v.save()
    v.plataformas.set(plataformas_ids)

    messages.success(request, 'Videojuego creado correctamente.')
    return redirect('detalle_videojuego', videojuego_id=v.id)

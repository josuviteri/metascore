from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Genero, Plataforma, Videojuego
# Create your views here.

def index(request):
    generos = Genero.objects.all()
    videojuegos_por_genero = {}

    for genero in generos:
        videojuego = Videojuego.objects.filter(genero=genero).order_by('-fecha_lanzamiento').first()
        videojuegos_por_genero[genero] = videojuego

    return render(request, 'index.html', {
        'videojuegos_por_genero': videojuegos_por_genero
    })

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
    return render(request, 'detalle_genero.html', {
        'genero': genero,
        'videojuegos': videojuegos
    })

def lista_plataformas(request):
    plataformas = Plataforma.objects.all()
    return render(request, 'plataformas.html', {'plataformas': plataformas})

def detalle_plataforma(request, plataforma_id):
    plataforma = get_object_or_404(Plataforma, pk=plataforma_id)
    videojuegos = plataforma.videojuego_set.all()
    return render(request, 'detalle_plataforma.html', {'plataforma': plataforma, 'videojuegos': videojuegos})

# --- NUEVO: mostrar formulario ---
def formulario(request):
    # GET: renderiza el formulario con datos para selects
    generos = Genero.objects.all().order_by('nombre')
    plataformas = Plataforma.objects.all().order_by('nombre')
    return render(request, 'formulario.html', {
        'generos': generos,
        'plataformas': plataformas
    })

# --- NUEVO: crear videojuego ---
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
    imagen_nombre = request.POST.get('imagen_nombre', '').strip()

    # Validaciones básicas
    if not titulo or not genero_id or not plataformas_ids or not fecha_lanzamiento or score is None:
        messages.error(request, 'Completa todos los campos obligatorios.')
        return redirect('formulario')

    try:
        genero = Genero.objects.get(pk=genero_id)
    except Genero.DoesNotExist:
        messages.error(request, 'El género seleccionado no existe.')
        return redirect('formulario')

    # Crear instancia
    v = Videojuego(
        titulo=titulo,
        genero=genero,
        descripcion=descripcion,
        # Fecha: si tu modelo se llama fecha_lanzamiento o fechalanzamiento, ajusta este nombre:
        fecha_lanzamiento=fecha_lanzamiento,  # ajusta si tu campo se llama distinto
        score=score
    )

    # Manejo de imagen: prioriza archivo; si no hay, usa nombre textual si lo soporta tu modelo
    if imagen_archivo:
        # Si tu modelo tiene ImageField/FileField llamado 'imagen', esto funciona:
        v.imagen = imagen_archivo
    elif imagen_nombre:
        # Si guardas solo el nombre/ruta (CharField) en el campo 'imagen', esto funciona;
        # si es ImageField con storage, deberías subir archivo en lugar de nombre.
        v.imagen = imagen_nombre

    v.save()

    # ManyToMany plataformas
    v.plataformas.set(plataformas_ids)

    messages.success(request, 'Videojuego creado correctamente.')
    return redirect('detalle_videojuego', videojuego_id=v.id)
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Videojuego, Genero, Plataforma
from .forms import VideojuegoForm

# 1. Vista de Inicio (Home)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mantenemos tu lógica original: mostrar el último juego de cada género
        videojuegos_por_genero = {}
        for genero in Genero.objects.all():
            juego = Videojuego.objects.filter(genero=genero).order_by('-fecha_lanzamiento').first()
            if juego:
                videojuegos_por_genero[genero] = juego
        
        context['videojuegos_por_genero'] = videojuegos_por_genero
        return context

# 2. Listados (Videojuegos, Géneros, Plataformas)
class VideojuegoListView(ListView):
    model = Videojuego
    template_name = 'videojuegos.html'
    context_object_name = 'videojuegos' # Así lo llamas en el HTML: {% for v in videojuegos %}

class GeneroListView(ListView):
    model = Genero
    template_name = 'generos.html'
    context_object_name = 'generos'

class PlataformaListView(ListView):
    model = Plataforma
    template_name = 'plataformas.html'
    context_object_name = 'plataformas'

# 3. Detalles (Ver un juego, ver un género, ver una plataforma)
class VideojuegoDetailView(DetailView):
    model = Videojuego
    template_name = 'detalle_videojuego.html'
    context_object_name = 'videojuego'

class GeneroDetailView(DetailView):
    model = Genero
    template_name = 'detalle_genero.html'
    context_object_name = 'genero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos los juegos de este género a la plantilla
        context['videojuegos'] = self.object.videojuego_set.all()
        return context

class PlataformaDetailView(DetailView):
    model = Plataforma
    template_name = 'detalle_plataforma.html'
    context_object_name = 'plataforma'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos los juegos de esta plataforma a la plantilla
        context['videojuegos'] = self.object.videojuego_set.all()
        return context

# 4. Formulario de Creación (Sustituye a tu antigua función 'sugerir_videojuego')
class VideojuegoCreateView(CreateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('videojuegos') # Redirige aquí al terminar
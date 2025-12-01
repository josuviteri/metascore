from django.contrib import messages
from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Videojuego, Genero, Plataforma, Contacto
from .forms import ContactForm, VideojuegoForm

# 1. Vista de Inicio (Home)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Mostrar el último juego publicado de cada género
        videojuegos_por_genero = {}
        for genero in Genero.objects.all():
            juego = (
                Videojuego.objects
                .filter(genero=genero)
                .order_by('-fecha_lanzamiento')
                .first()
            )
            if juego:
                videojuegos_por_genero[genero] = juego

        context['videojuegos_por_genero'] = videojuegos_por_genero
        return context

# 2. Listados (videojuegos, géneros, plataformas)
class VideojuegoListView(ListView):
    template_name = 'videojuegos.html'
    context_object_name = 'videojuegos'

    def get_queryset(self):
        return get_list_or_404(Videojuego)

class GeneroListView(ListView):
    template_name = 'generos.html'
    context_object_name = 'generos'

    def get_queryset(self):
        return get_list_or_404(Genero)

class PlataformaListView(ListView):
    template_name = 'plataformas.html'
    context_object_name = 'plataformas'

    def get_queryset(self):
        return get_list_or_404(Plataforma)

# 3. Detalles
class VideojuegoDetailView(DetailView):
    model = Videojuego
    template_name = 'detalle_videojuego.html'
    context_object_name = 'videojuego'

class GeneroDetailView(DetailView):
    model = Genero
    template_name = 'detalle_genero.html'
    context_object_name = 'genero'

class PlataformaDetailView(DetailView):
    model = Plataforma
    template_name = 'detalle_plataforma.html'
    context_object_name = 'plataforma'

# 4. Formularios
class VideojuegoCreateView(CreateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'formulario.html'
    success_url = reverse_lazy('videojuegos')

class ContactoView(CreateView):
    model = Contacto
    form_class = ContactForm
    template_name = "formulario_contacto.html"
    success_url = reverse_lazy('formulario_contacto')

    def form_valid(self, form):
        messages.success(self.request, "Tu mensaje ha sido enviado y guardado correctamente.")
        return super().form_valid(form)

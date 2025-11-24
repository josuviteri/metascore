from django.contrib import admin
from django.utils.html import format_html
from .models import Genero, Plataforma, Videojuego

# --- 1. CONFIGURACIÓN DEL DISEÑO GENERAL ---
# Cambiamos los textos del encabezado para que parezca una app profesional
admin.site.site_header = "Administración de MetaScore"  # Texto en la barra superior
admin.site.site_title = "MetaScore Admin"               # Título en la pestaña del navegador
admin.site.index_title = "Panel de Gestión"             # Título de la página principal

# --- 2. PERSONALIZACIÓN DE MODELOS ---

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contar_juegos')
    search_fields = ('nombre',)
    ordering = ('nombre',)

    def contar_juegos(self, obj):
        # Muestra cuántos juegos hay de este género
        return obj.videojuego_set.count()
    contar_juegos.short_description = "Nº Videojuegos"

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contar_juegos')
    search_fields = ('nombre',)

    def contar_juegos(self, obj):
        return obj.videojuego_set.count()
    contar_juegos.short_description = "Nº Videojuegos"

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista
    list_display = ('mostrar_imagen', 'titulo', 'genero', 'fecha_lanzamiento', 'score_color')
    
    # Menú lateral de filtros
    list_filter = ('genero', 'plataformas', 'fecha_lanzamiento')
    
    # Barra de búsqueda
    search_fields = ('titulo', 'descripcion')
    
    # Navegación por fechas arriba de la lista
    date_hierarchy = 'fecha_lanzamiento'
    
    # Edición rápida desde la lista
    list_editable = ('fecha_lanzamiento',)
    
    # Widget mejorado para seleccionar muchas plataformas
    filter_horizontal = ('plataformas',)
    
    # Paginación (útil si tienes muchos juegos)
    list_per_page = 10

    # Función para mostrar la imagen en pequeñito
    def mostrar_imagen(self, obj):
        if obj.imagen:
            # Asumimos que la imagen está en /static/images/
            return format_html(
                '<img src="/static/images/{}" width="50" height="50" style="object-fit:cover; border-radius:4px;" />',
                obj.imagen
            )
        return "-"
    mostrar_imagen.short_description = "Portada"

    # Función para colorear el score según la nota
    def score_color(self, obj):
        if obj.score is None:
            return "-"
        color = "red"
        if obj.score >= 90:
            color = "green"
        elif obj.score >= 70:
            color = "orange"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.score)
    score_color.short_description = "Score"
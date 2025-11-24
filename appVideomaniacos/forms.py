from django import forms
from .models import Videojuego, Contacto

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'genero', 'plataformas', 'fecha_lanzamiento', 'score', 'imagen', 'descripcion']
        
        # Añadimos clases CSS para que se vea igual de bonito que tu HTML actual
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Hollow Knight'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'plataformas': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
            'fecha_lanzamiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100', 'min': 0, 'max': 100}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Resumen del videojuego...'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'fecha_lanzamiento': 'Fecha de lanzamiento',
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']

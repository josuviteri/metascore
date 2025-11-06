from django.db import models

class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Plataforma(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    titulo = models.CharField(max_length=200)  # 👈 cambio de 'nombre' a 'titulo'
    descripcion = models.TextField(blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    plataformas = models.ManyToManyField(Plataforma)
    imagen = models.ImageField(upload_to='videojuegos/', blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)  # 👈 nuevo campo
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.titulo

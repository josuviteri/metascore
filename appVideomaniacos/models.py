from django.db import models

class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Plataforma(models.Model):
    nombre = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_lanzamiento = models.DateField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    plataformas = models.ManyToManyField(Plataforma)
    imagen = models.URLField(blank=True)

    def __str__(self):
        return self.titulo

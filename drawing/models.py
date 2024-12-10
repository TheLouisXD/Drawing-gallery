from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dibujo(models.Model):
    titulo = models.CharField(max_length=100, default='Sin titulo', verbose_name='Titulo del dibujo')
    imagen = models.ImageField(upload_to='dibujos/', verbose_name='Imagen del dibujo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion del dibujo')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creador del dibujo')
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name='Categoria del dibujo')

    # Funcion para calcular los votos del dibujo
    def total_estrellas(self):
        # la variable estrella_set es una relacion inversa creada automáticamente por Django
        return self.estrella_set.count()
    
    def __str__(self) -> str:
        return f"{self.titulo} creado por {self.usuario.username}"

class Estrella(models.Model):
    dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE, verbose_name="Dibujo asignado a la estrella")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que ha hecho la estrella")

    def __str__(self):
        return f"{self.usuario.username} ha hecho una estrella en {self.dibujo.titulo}"

class Comentario(models.Model):
    dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE, verbose_name="Dibujo al que se le ha añadido el comentario")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que ha añadido el comentario")
    texto = models.TextField(max_length=256, verbose_name="Texto del comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación del comentario")
    
    def __str__(self):
        return f"{self.usuario.username} ha añadido un comentario en {self.dibujo.titulo}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoria")
    descripcion = models.TextField(max_length=1000, verbose_name="Descripción de la categoria")
    lista_dibujos = models.ManyToManyField(Dibujo, related_name='categorias', verbose_name="Lista de dibujos en la categoria", blank=True)

    def __str__(self):
        return self.nombre

class Reporte(models.Model):
    dibujo = models.ForeignKey(Dibujo, on_delete=models.CASCADE, verbose_name="Dibujo que ha sio reportado")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que ha reportado el dibujo")
    motivo = models.TextField(max_length=256, verbose_name="Motivo del reporte")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del reporte")

    def __str__(self):
        return f"{self.usuario.username} ha reportado el dibujo {self.dibujo.titulo}"

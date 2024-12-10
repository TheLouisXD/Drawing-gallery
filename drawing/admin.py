from django.contrib import admin
from .models import Dibujo, Estrella, Comentario, Categoria, Reporte

# Register your models here.
admin.site.register(Dibujo)
admin.site.register(Estrella)
admin.site.register(Comentario)
admin.site.register(Categoria) 
admin.site.register(Reporte)
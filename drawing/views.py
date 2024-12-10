from django.shortcuts import render, redirect
from django.db import models
from .models import Dibujo, Estrella, Comentario, Categoria, Reporte
from .serializer import DibujoSerializer

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import base64
from django.core.files.base import ContentFile

# Django filters
from django_filters import views
from django_filters import FilterSet, ModelChoiceFilter, OrderingFilter

# Filters
class DibujoFilter(FilterSet):
    categoria = ModelChoiceFilter(
        queryset = Categoria.objects.all(),
        to_field_name = 'nombre',
        label = 'Categoria',
    )

    order_by = OrderingFilter(
        fields = (
            ('fecha_creacion', 'fecha_creacion'),
        ),
        field_labels = {
            'fecha_creacion': 'Fecha de creación (ascendente)',
            '-fecha_creacion': 'Fecha de creación (descendente)'
        }
    )

    class Meta:
        model = Dibujo
        fields = ['categoria', 'order_by']

class GaleriaView(views.FilterView):
    model = Dibujo
    template_name = 'galeria/main.html'
    filterset_class = DibujoFilter
    context_object_name = 'dibujos'

    def get_queryset(self):
        queryset = super().get_queryset()

        ordering = self.request.GET.get('order_by', '-fecha_creacion')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


# Create your views here.
def index(request):
    # obtener los 5 dibujos más votados
    dibujos_mas_votados = Dibujo.objects.annotate(num_estrellas=models.Count('estrella')).order_by('-num_estrellas')[:5]
    
    # obtener los 5 dibujos más recientes
    dibujos_mas_recientes = Dibujo.objects.order_by('-fecha_creacion')[:5]

    context = {
        'dibujos_mas_votados': dibujos_mas_votados,
        'dibujos_mas_recientes': dibujos_mas_recientes,
    }

    return render(request, 'index.html', context)

def crear_dibujo(request):
    if request.method == 'POST':
        usuario = request.user
        titulo = request.POST['titulo']
        categoria_id = request.POST['categoria']
        categoria = Categoria.objects.get(id = categoria_id)
        imagen_base64 = request.POST['imagen']

        # decodificar la imagen
        format, imgstr = imagen_base64.split(';base64,')
        ext = format.split('/')[-1]
        imagen = ContentFile(base64.b64decode(imgstr), name=f'dibujo_{titulo}.{ext}')

        # guardamos la foto en la base de datos
        Dibujo.objects.create(titulo = titulo, categoria = categoria, imagen = imagen, usuario = usuario)
        return redirect('index')
    
    context = {
        'categorias': Categoria.objects.all(),
    }

    return render(request, 'dibujo/main.html', context)

def galeria(request):
    dibujos = Dibujo.objects.all()
    context = {
        'dibujos': dibujos,
    }
    return render(request, 'galeria/main.html', context)

def detalle_dibujo(request, dibujo_id):
    dibujo = Dibujo.objects.get(id = dibujo_id)
    comentarios = Comentario.objects.filter(dibujo = dibujo).order_by('fecha_creacion')
    usuario_ha_votado = False

    if request.user.is_authenticated:
    
        usuario_ha_votado = Estrella.objects.filter(dibujo = dibujo, usuario = request.user).exists()
    
    context = {
        'dibujo': dibujo,
        'comentarios': comentarios,
        'usuario_ha_votado': usuario_ha_votado,
    }

    return render(request, 'dibujo/detalle.html', context)

@login_required
def votar_dibujo(request, dibujo_id):
    if request.method == 'POST':
        dibujo = Dibujo.objects.get(id = dibujo_id)
        estrella, created = Estrella.objects.get_or_create(
            dibujo = dibujo, 
            usuario = request.user
        )

        if not created:
            estrella.delete()
            return  JsonResponse({'status': 'removed', 'total_estrellas': dibujo.total_estrellas()})
        
        return JsonResponse({'status': 'added', 'total_estrellas': dibujo.total_estrellas()})

@login_required
def comentar_dibujo(request, dibujo_id):
    if request.method == 'POST':
        dibujo = Dibujo.objects.get(id = dibujo_id)
        texto = request.POST.get('texto')

        if texto:
            comentario = Comentario.objects.create(
                dibujo = dibujo,
                usuario = request.user,
                texto = texto
            )

            return JsonResponse({
                'status': 'success',
                'comentario_id': comentario.id,
                'usuario': comentario.usuario.username,
                'texto': comentario.texto,
                'fecha': comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            })
        
    return JsonResponse({'status': 'error'}, status = 400)
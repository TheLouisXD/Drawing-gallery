from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import GaleriaView, galeria

urlpatterns = [
    path('', views.index, name='index'),
    # Dibujos
    path('crear', views.crear_dibujo, name='crear_dibujo'),
    path('galeria', GaleriaView.as_view(), name='galeria'),
    path('dibujo/<int:dibujo_id>/', views.detalle_dibujo, name='detalle_dibujo'),
    path('dibujo/<int:dibujo_id>/votar/', views.votar_dibujo, name='votar_dibujo'),
    path('dibujo/<int:dibujo_id>/comentar/', views.comentar_dibujo, name='comentar_dibujo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
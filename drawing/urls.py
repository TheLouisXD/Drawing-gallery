from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import GaleriaView, galeria, DrawingCountView, DrawingListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'),
    # Dibujos
    path('crear', views.crear_dibujo, name='crear_dibujo'),
    path('galeria', GaleriaView.as_view(), name='galeria'),
    path('dibujo/<int:dibujo_id>/', views.detalle_dibujo, name='detalle_dibujo'),
    path('dibujo/<int:dibujo_id>/votar/', views.votar_dibujo, name='votar_dibujo'),
    path('dibujo/<int:dibujo_id>/comentar/', views.comentar_dibujo, name='comentar_dibujo'),
    path('dibujo/exportar/', views.exportar_dibujos_page,name='exportar_dibujos_page'),
    path('dibujo/exportar/csv', views.exportar_dibujos, name='exportar_dibujos'),
    # Reportes
    path('dibujo/reportar/<int:dibujo_id>/', views.reportar_dibujo, name='reportar_dibujo'),
    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Drawing count endpoint
    path('api/drawings/count/', DrawingCountView.as_view(), name='drawing-count'),
    # Drawings list
    path('api/drawings/', DrawingListView.as_view(), name='Drawnings list view' ),
    path('delete/<int:dibujo_id>/', views.delete_dibujo, name='delete_dibujo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
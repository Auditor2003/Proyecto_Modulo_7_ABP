from django.urls import path
from .views import (
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView
)

urlpatterns = [
    # Lista de usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),

    # Crear usuario
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),

    # Editar usuario
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),

    # Eliminar usuario
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),
]

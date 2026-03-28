from django.urls import path
from .views import UsuarioListView, UsuarioCreateView, UsuarioUpdateView

urlpatterns = [
    # Aquí dejo la lista de usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),

    # Aquí dejo la creación de usuarios
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),

    # Aquí agrego la edición de usuario (uso el id del usuario)
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
]

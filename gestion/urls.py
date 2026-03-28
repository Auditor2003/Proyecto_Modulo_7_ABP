from django.urls import path
from .views import UsuarioListView, UsuarioCreateView

urlpatterns = [
    # Aquí dejo la ruta para listar usuarios
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),

    # Aquí agrego la ruta para crear un nuevo usuario
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),
]
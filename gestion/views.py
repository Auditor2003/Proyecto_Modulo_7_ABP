from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Usuario


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Aquí estoy mostrando todos los usuarios en una lista simple
    # Uso context_object_name para poder recorrerlos fácil en el template


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    fields = ['nombre', 'correo_electronico', 'contrasena', 'saldo']
    success_url = reverse_lazy('usuario_list')

    # Aquí estoy creando un formulario automático con los campos del modelo
    # Cuando el usuario envía el formulario, se guarda en la BD
    # Después redirijo a la lista de usuarios
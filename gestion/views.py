from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Usuario


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Aquí estoy mostrando todos los usuarios en una lista simple


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    fields = ['nombre', 'correo_electronico', 'contrasena']
    success_url = reverse_lazy('usuario_list')

    # Aquí defino solo los campos que el usuario debería ingresar
    # Excluyo saldo porque se maneja internamente en el sistema
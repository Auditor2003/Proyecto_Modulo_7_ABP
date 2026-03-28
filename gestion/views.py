from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Usuario
from .forms import UsuarioForm


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Aquí estoy mostrando todos los usuarios en una lista simple


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Aquí uso un formulario personalizado en lugar de fields
    # Esto me permite agregar validaciones como confirmación de contraseña
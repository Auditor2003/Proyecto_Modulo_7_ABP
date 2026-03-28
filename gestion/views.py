from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Usuario
from .forms import UsuarioForm


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Aquí muestro todos los usuarios


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Aquí creo usuarios con validación personalizada


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Aquí edito usuarios reutilizando el mismo formulario


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    # Aquí elimino un usuario con confirmación previa
from django.views.generic import ListView
from .models import Usuario


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

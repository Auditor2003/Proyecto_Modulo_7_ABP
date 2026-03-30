from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .models import Usuario, Transaccion, Moneda
from .forms import UsuarioForm, TransaccionForm


# CRUD USUARIO

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Muestro todos los usuarios


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Creo usuarios con validación personalizada


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Edito usuarios reutilizando el mismo formulario


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    # Elimino un usuario con confirmación previa


# CRUD MONEDA

class MonedaListView(ListView):
    model = Moneda
    template_name = 'gestion/moneda_list.html'
    context_object_name = 'monedas'

    # Muestro todas las monedas


class MonedaCreateView(CreateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')

    # Creo una nueva moneda


class MonedaUpdateView(UpdateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')

    # Edito una moneda existente


class MonedaDeleteView(DeleteView):
    model = Moneda
    template_name = 'gestion/moneda_confirm_delete.html'
    success_url = reverse_lazy('moneda_list')

    # Elimino una moneda


# LIST TRANSACCION

class TransaccionListView(ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'

    # Muestro todas las transacciones


# CREATE TRANSACCION

class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')

    # Sobrescribo form_valid para aplicar lógica de negocio
    def form_valid(self, form):

        emisor = form.cleaned_data['id_usuario_emisor']
        receptor = form.cleaned_data['id_usuario_receptor']
        importe = form.cleaned_data['importe']
        moneda = form.cleaned_data['currency_id']

        # Valido que no sea el mismo usuario
        if emisor == receptor:
            messages.error(self.request, "No puedes transferirte a ti mismo.")
            return self.form_invalid(form)

        # Valido saldo suficiente
        if emisor.saldo < importe:
            messages.error(self.request, "Saldo insuficiente.")
            return self.form_invalid(form)

        try:
            with transaction.atomic():

                # Descuento saldo al emisor
                emisor.saldo -= importe
                emisor.save()

                # Sumo saldo al receptor
                receptor.saldo += importe
                receptor.save()

                # Guardo la transaccion
                response = super().form_valid(form)

            messages.success(self.request, "Transacción realizada correctamente.")
            return response

        except Exception as e:
            messages.error(self.request, f"Error al procesar la transacción: {str(e)}")
            return self.form_invalid(form)
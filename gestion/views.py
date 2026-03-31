from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .models import Usuario, Transaccion, Moneda, Beneficiario
from .forms import UsuarioForm, TransaccionForm, BeneficiarioForm, DepositoForm


# USUARIO

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'

    # Muestro todos los usuarios registrados


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Creo un nuevo usuario


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Permito editar usuarios existentes


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    # Elimino un usuario con confirmación


# MONEDA

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

    # Creo una moneda


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


# BENEFICIARIO

class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('transaccion_create')

    # Creo un beneficiario desde el flujo de transacción y vuelvo al formulario


# TRANSACCIONES

class TransaccionListView(ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'

    # Muestro todas las transacciones realizadas


class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')

    # Aplico la lógica de negocio al crear una transacción
    def form_valid(self, form):

        emisor = form.cleaned_data['id_usuario_emisor']
        importe = form.cleaned_data['importe']

        # Valido que el usuario tenga saldo suficiente
        if emisor.saldo < importe:
            messages.error(self.request, "Saldo insuficiente.")
            return self.form_invalid(form)

        try:
            with transaction.atomic():

                # Descuento saldo al emisor
                emisor.saldo -= importe
                emisor.save()

                # Registro la transacción
                response = super().form_valid(form)

            messages.success(self.request, "Transacción realizada correctamente.")
            return response

        except Exception as e:
            messages.error(self.request, f"Error: {str(e)}")
            return self.form_invalid(form)


# DEPOSITO

class DepositoCreateView(FormView):
    template_name = 'gestion/deposito_form.html'
    form_class = DepositoForm
    success_url = reverse_lazy('usuario_list')

    # Proceso el depósito y aumento el saldo del usuario
    def form_valid(self, form):

        usuario = form.cleaned_data['usuario']
        monto = form.cleaned_data['monto']

        try:
            with transaction.atomic():

                # Sumo saldo al usuario
                usuario.saldo += monto
                usuario.save()

            messages.success(
                self.request,
                f"Depósito realizado correctamente. Nuevo saldo: {usuario.saldo}"
            )

            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error al realizar depósito: {str(e)}")
            return self.form_invalid(form)
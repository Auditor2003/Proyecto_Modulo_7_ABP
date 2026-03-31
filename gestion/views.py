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

    # Muestro todos los usuarios


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Creo un usuario


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')

    # Edito usuario


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    # Elimino usuario


# MONEDA

class MonedaListView(ListView):
    model = Moneda
    template_name = 'gestion/moneda_list.html'
    context_object_name = 'monedas'

    # Muestro monedas


class MonedaCreateView(CreateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')

    # Creo moneda


class MonedaUpdateView(UpdateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')

    # Edito moneda


class MonedaDeleteView(DeleteView):
    model = Moneda
    template_name = 'gestion/moneda_confirm_delete.html'
    success_url = reverse_lazy('moneda_list')

    # Elimino moneda


# BENEFICIARIO (CRUD COMPLETO)

class BeneficiarioListView(ListView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_list.html'
    context_object_name = 'beneficiarios'

    # Muestro beneficiarios


class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')

    # Creo beneficiario


class BeneficiarioUpdateView(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')

    # Edito beneficiario


class BeneficiarioDeleteView(DeleteView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_confirm_delete.html'
    success_url = reverse_lazy('beneficiario_list')

    # Elimino beneficiario


# TRANSACCIONES

class TransaccionListView(ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'

    # Muestro historial


class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')

    # Creo transacción y descuento saldo
    def form_valid(self, form):

        emisor = form.cleaned_data['id_usuario_emisor']
        importe = form.cleaned_data['importe']

        if emisor.saldo < importe:
            messages.error(self.request, "Saldo insuficiente.")
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                emisor.saldo -= importe
                emisor.save()
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

    # Sumo saldo y registro movimiento
    def form_valid(self, form):

        usuario = form.cleaned_data['usuario']
        monto = form.cleaned_data['monto']

        try:
            with transaction.atomic():

                beneficiario, _ = Beneficiario.objects.get_or_create(
                    nombre="DEPOSITO"
                )

                usuario.saldo += monto
                usuario.save()

                Transaccion.objects.create(
                    id_usuario_emisor=usuario,
                    id_beneficiario=beneficiario,
                    currency_id=Moneda.objects.first(),
                    importe=monto
                )

            messages.success(
                self.request,
                f"Depósito realizado correctamente. Nuevo saldo: {usuario.saldo}"
            )

            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error al realizar depósito: {str(e)}")
            return self.form_invalid(form)


# CARTOLA

class CartolaUsuarioView(ListView):
    model = Transaccion
    template_name = 'gestion/cartola.html'
    context_object_name = 'movimientos'

    # Filtro movimientos por usuario
    def get_queryset(self):
        usuario_id = self.kwargs.get('usuario_id')
        return Transaccion.objects.filter(
            id_usuario_emisor_id=usuario_id
        ).order_by('-fecha_transaccion')

    # Envío usuario (para saldo)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_id = self.kwargs.get('usuario_id')
        context['usuario'] = Usuario.objects.get(user_id=usuario_id)
        return context
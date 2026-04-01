# IMPORTACIONES

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
import requests

from .models import Usuario, Transaccion, Moneda, Beneficiario
from .forms import UsuarioForm, TransaccionForm, BeneficiarioForm, DepositoForm


# USUARIO

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestion/usuario_list.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'gestion/usuario_form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_list')


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestion/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if Transaccion.objects.filter(id_usuario_emisor=self.object).exists():
            messages.error(
                request,
                "No se puede eliminar este usuario porque tiene transacciones registradas."
            )
            return redirect('usuario_list')

        return super().post(request, *args, **kwargs)


# MONEDA

class MonedaListView(ListView):
    model = Moneda
    template_name = 'gestion/moneda_list.html'
    context_object_name = 'monedas'


class MonedaCreateView(CreateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')


class MonedaUpdateView(UpdateView):
    model = Moneda
    template_name = 'gestion/moneda_form.html'
    fields = ['nombre_moneda', 'simbolo']
    success_url = reverse_lazy('moneda_list')


class MonedaDeleteView(DeleteView):
    model = Moneda
    template_name = 'gestion/moneda_confirm_delete.html'
    success_url = reverse_lazy('moneda_list')


# BENEFICIARIO

class BeneficiarioListView(ListView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_list.html'
    context_object_name = 'beneficiarios'

    def get_queryset(self):
        return Beneficiario.objects.exclude(nombre="DEPOSITO")


class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')


class BeneficiarioUpdateView(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')


class BeneficiarioDeleteView(DeleteView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_confirm_delete.html'
    success_url = reverse_lazy('beneficiario_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if Transaccion.objects.filter(id_beneficiario=self.object).exists():
            messages.error(
                request,
                "No se puede eliminar este beneficiario porque tiene transacciones asociadas."
            )
            return redirect('beneficiario_list')

        return super().post(request, *args, **kwargs)


# TRANSACCIONES

class TransaccionListView(ListView):
    model = Transaccion
    template_name = 'gestion/transaccion_list.html'
    context_object_name = 'transacciones'


class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')

    def form_valid(self, form):
        emisor = form.cleaned_data['id_usuario_emisor']
        importe = form.cleaned_data['importe']

        if emisor.saldo < importe:
            messages.error(
                self.request,
                f"Saldo insuficiente. Saldo actual: {emisor.saldo}"
            )
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

    def form_valid(self, form):
        usuario = form.cleaned_data['usuario']
        monto = form.cleaned_data['monto']

        moneda = Moneda.objects.first()

        if not moneda:
            messages.error(
                self.request,
                "Debe crear una moneda antes de realizar depósitos."
            )
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                beneficiario, _ = Beneficiario.objects.get_or_create(nombre="DEPOSITO")

                usuario.saldo += monto
                usuario.save()

                Transaccion.objects.create(
                    id_usuario_emisor=usuario,
                    id_beneficiario=beneficiario,
                    currency_id=moneda,
                    importe=monto
                )

            messages.success(
                self.request,
                f"Depósito realizado correctamente. Nuevo saldo: {usuario.saldo}"
            )

            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error: {str(e)}")
            return self.form_invalid(form)


# CARTOLA

class CartolaUsuarioView(ListView):
    model = Transaccion
    template_name = 'gestion/cartola.html'
    context_object_name = 'movimientos'

    def get_queryset(self):
        usuario_id = self.kwargs.get('usuario_id')
        return Transaccion.objects.filter(
            id_usuario_emisor_id=usuario_id
        ).order_by('-fecha_transaccion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_id = self.kwargs.get('usuario_id')
        context['usuario'] = Usuario.objects.get(user_id=usuario_id)
        return context


# DASHBOARD

class DashboardView(ListView):
    model = Usuario
    template_name = 'gestion/dashboard.html'
    context_object_name = 'usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hay_usuarios'] = Usuario.objects.exists()
        context['hay_monedas'] = Moneda.objects.exists()

        try:
            response = requests.get("https://mindicador.cl/api")
            data = response.json()

            context['dolar'] = data['dolar']['valor']
            context['uf'] = data['uf']['valor']
            context['euro'] = data['euro']['valor']

        except:
            context['dolar'] = 'N/D'
            context['uf'] = 'N/D'
            context['euro'] = 'N/D'

        return context
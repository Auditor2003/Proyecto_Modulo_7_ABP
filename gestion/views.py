from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .models import Usuario, Transaccion, Moneda, Beneficiario
from .forms import UsuarioForm, TransaccionForm, BeneficiarioForm


# 
# CRUD USUARIO
# 

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


# 
# CRUD MONEDA
#

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


# 
# CRUD BENEFICIARIO 
#

class BeneficiarioListView(ListView):
    model = Beneficiario
    template_name = 'gestion/beneficiario_list.html'
    context_object_name = 'beneficiarios'

    # Muestro todos los beneficiarios


class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'gestion/beneficiario_form.html'
    success_url = reverse_lazy('beneficiario_list')

    # Creo beneficiario desde la web


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


class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'gestion/transaccion_form.html'
    success_url = reverse_lazy('transaccion_list')

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
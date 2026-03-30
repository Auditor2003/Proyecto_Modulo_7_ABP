from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db import transaction

from .models import Transaccion, Usuario
from .forms import TransaccionForm


class CrearTransaccionView(View):

    def get(self, request):
        # Yo muestro el formulario vacío
        formulario = TransaccionForm()
        return render(request, 'transacciones/crear.html', {'formulario': formulario})

    def post(self, request):
        # Yo recibo los datos del formulario
        formulario = TransaccionForm(request.POST)

        if formulario.is_valid():
            # Yo obtengo los datos validados
            emisor = formulario.cleaned_data['emisor']
            receptor = formulario.cleaned_data['receptor']
            monto = formulario.cleaned_data['monto']

            # Yo valido que no sea el mismo usuario
            if emisor == receptor:
                messages.error(request, "No puedes transferirte a ti mismo.")
                return render(request, 'transacciones/crear.html', {'formulario': formulario})

            # Yo valido saldo suficiente
            if emisor.saldo < monto:
                messages.error(request, "Saldo insuficiente.")
                return render(request, 'transacciones/crear.html', {'formulario': formulario})

            try:
                # Yo aseguro que todo ocurra correctamente o nada ocurra
                with transaction.atomic():

                    # Yo descuento saldo al emisor
                    emisor.saldo -= monto
                    emisor.save()

                    # Yo sumo saldo al receptor
                    receptor.saldo += monto
                    receptor.save()

                    # Yo registro la transacción
                    Transaccion.objects.create(
                        emisor=emisor,
                        receptor=receptor,
                        monto=monto
                    )

                messages.success(request, "Transacción realizada correctamente.")
                return redirect('lista_transacciones')

            except Exception as e:
                # Yo capturo errores inesperados
                messages.error(request, f"Error al procesar la transacción: {str(e)}")

        # Yo retorno el formulario con errores
        return render(request, 'transacciones/crear.html', {'formulario': formulario})
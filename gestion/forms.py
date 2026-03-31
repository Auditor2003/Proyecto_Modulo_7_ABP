from django import forms
from .models import Usuario, Transaccion, Beneficiario



# FORM USUARIO

class UsuarioForm(forms.ModelForm):
    # Agrego campo para confirmar contraseña
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'contrasena']

        # Oculto la contraseña en el input
        widgets = {
            'contrasena': forms.PasswordInput(),
        }

    def clean(self):
        # Obtengo los datos del formulario
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar = cleaned_data.get("confirmar_contrasena")

        # Valido que ambas contraseñas coincidan
        if contrasena and confirmar and contrasena != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Valido longitud mínima
        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        return cleaned_data



# FORM BENEFICIARIO


class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ['nombre', 'detalle']

    # Uso este formulario para crear beneficiarios sin login


# FORM TRANSACCION

class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        fields = [
            'id_usuario_emisor',
            'id_beneficiario',
            'currency_id',
            'importe'
        ]

    def clean(self):
        # Obtengo los datos del formulario
        cleaned_data = super().clean()

        emisor = cleaned_data.get('id_usuario_emisor')
        importe = cleaned_data.get('importe')

        # Valido que el monto sea mayor a 0
        if importe and importe <= 0:
            raise forms.ValidationError("El importe debe ser mayor a 0.")

        # Valido saldo suficiente
        if emisor and importe and emisor.saldo < importe:
            raise forms.ValidationError("El emisor no tiene saldo suficiente.")

        return cleaned_data


# FORM DEPOSITO 


class DepositoForm(forms.Form):

    # Selecciono el usuario que recibirá el depósito
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Usuario"
    )

    # Monto a depositar
    monto = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=0.01,
        label="Monto a depositar"
    )

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        # Validación extra de seguridad
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a 0.")

        return monto
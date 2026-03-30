from django import forms
from .models import Usuario, Transaccion, Beneficiario


class UsuarioForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'contrasena']

        widgets = {
            'contrasena': forms.PasswordInput(),
        }

    def clean(self):
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
        cleaned_data = super().clean()

        emisor = cleaned_data.get('id_usuario_emisor')
        importe = cleaned_data.get('importe')

        # Valido que el importe sea mayor a 0
        if importe and importe <= 0:
            raise forms.ValidationError("El importe debe ser mayor a 0.")

        # Valido saldo suficiente
        if emisor and importe and emisor.saldo < importe:
            raise forms.ValidationError("El emisor no tiene saldo suficiente.")

        return cleaned_data
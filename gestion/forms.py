from django import forms
from .models import Usuario, Transaccion


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

        # Valido que la contraseña tenga una longitud mínima
        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        return cleaned_data


# FORM TRANSACCION

class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        fields = [
            'id_usuario_emisor',
            'id_usuario_receptor',
            'currency_id',
            'importe'
        ]

    def clean(self):
        cleaned_data = super().clean()

        emisor = cleaned_data.get('id_usuario_emisor')
        receptor = cleaned_data.get('id_usuario_receptor')
        importe = cleaned_data.get('importe')

        # Valido que el emisor y receptor no sean el mismo usuario
        if emisor and receptor and emisor == receptor:
            raise forms.ValidationError("No puedes transferirte a ti mismo.")

        # Valido que el importe sea mayor que cero
        if importe and importe <= 0:
            raise forms.ValidationError("El importe debe ser mayor a 0.")

        # Valido que el emisor tenga saldo suficiente
        if emisor and importe and emisor.saldo < importe:
            raise forms.ValidationError("El emisor no tiene saldo suficiente.")

        return cleaned_data
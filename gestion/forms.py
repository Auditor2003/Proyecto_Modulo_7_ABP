from django import forms
from .models import Usuario


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

        # Aquí valido que ambas contraseñas coincidan
        if contrasena and confirmar and contrasena != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Aquí aplico una validación básica de seguridad
        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        return cleaned_data
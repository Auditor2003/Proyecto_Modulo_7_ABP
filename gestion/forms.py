from django import forms
from .models import Usuario, Transaccion, Beneficiario


class UsuarioForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'contrasena']

        widgets = {
            'contrasena': forms.PasswordInput(),
        }

        labels = {
            'correo_electronico': 'Correo Electrónico',
            'contrasena': 'Contraseña',
        }

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar = cleaned_data.get("confirmar_contrasena")

        if contrasena and confirmar and contrasena != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")

        return cleaned_data


class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ['nombre', 'detalle']


class TransaccionForm(forms.ModelForm):
    id_beneficiario = forms.ModelChoiceField(
        queryset=Beneficiario.objects.exclude(nombre="DEPOSITO"),
        label="Beneficiario"
    )

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

        if importe and importe <= 0:
            raise forms.ValidationError("El importe debe ser mayor a 0.")

        if emisor and importe and emisor.saldo < importe:
            raise forms.ValidationError("El emisor no tiene saldo suficiente.")

        return cleaned_data


class DepositoForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Usuario"
    )

    monto = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=0.01,
        label="Monto a depositar"
    )

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')

        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a 0.")

        return monto
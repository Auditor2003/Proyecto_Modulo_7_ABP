from django.db import models
from django.core.exceptions import ValidationError


class Moneda(models.Model):
    currency_id = models.AutoField(primary_key=True)
    nombre_moneda = models.CharField(max_length=50)
    simbolo = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_moneda


class Usuario(models.Model):
    user_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=255)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Beneficiario(models.Model):
    # Este modelo representa a personas que reciben dinero sin tener login
    beneficiario_id = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=100)

    # Campo opcional por si quieres extender después (email, alias, etc.)
    detalle = models.CharField(max_length=150, blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Transaccion(models.Model):
    transaction_id = models.AutoField(primary_key=True)

    # Emisor SIEMPRE es un usuario del sistema
    id_usuario_emisor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='transacciones_enviadas'
    )

    # Receptor ahora es Beneficiario (cambio de arquitectura)
    id_beneficiario = models.ForeignKey(
        Beneficiario,
        on_delete=models.CASCADE,
        related_name='transacciones_recibidas'
    )

    currency_id = models.ForeignKey(
        Moneda,
        on_delete=models.CASCADE
    )

    importe = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['id_usuario_emisor', 'fecha_transaccion']),
            models.Index(fields=['id_beneficiario', 'fecha_transaccion']),
        ]

    def clean(self):
        # Validación de monto
        if self.importe <= 0:
            raise ValidationError("El importe debe ser mayor que 0.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_usuario_emisor} -> {self.id_beneficiario} : {self.importe}"
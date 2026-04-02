from django.contrib import admin
from .models import Usuario, Moneda, Transaccion, Beneficiario

admin.site.register(Usuario)
admin.site.register(Moneda)
admin.site.register(Transaccion)
admin.site.register(Beneficiario)

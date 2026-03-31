from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario_list'),

    # CRUD Usuario completo
    path('crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),

    # Moneda
    path('moneda/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/crear/', MonedaCreateView.as_view(), name='moneda_create'),

    # Transacciones
    path('transaccion/', TransaccionListView.as_view(), name='transaccion_list'),
    path('transaccion/crear/', TransaccionCreateView.as_view(), name='transaccion_create'),

    # Beneficiario
    path('beneficiario/crear/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),
]
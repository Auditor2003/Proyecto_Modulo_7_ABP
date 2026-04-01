from django.urls import path
from .views import *


urlpatterns = [

    # HOME (dashboard principal)
    path('', DashboardView.as_view(), name='home'),

    # USUARIO
    path('usuarios/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),

    # MONEDA
    path('moneda/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/crear/', MonedaCreateView.as_view(), name='moneda_create'),
    path('moneda/editar/<int:pk>/', MonedaUpdateView.as_view(), name='moneda_update'),
    path('moneda/eliminar/<int:pk>/', MonedaDeleteView.as_view(), name='moneda_delete'),

    # TRANSACCIONES
    path('transaccion/', TransaccionListView.as_view(), name='transaccion_list'),
    path('transaccion/crear/', TransaccionCreateView.as_view(), name='transaccion_create'),

    # DEPOSITO
    path('deposito/', DepositoCreateView.as_view(), name='deposito_create'),

    # CARTOLA
    path('cartola/<int:usuario_id>/', CartolaUsuarioView.as_view(), name='cartola_usuario'),

    # BENEFICIARIO
    path('beneficiario/', BeneficiarioListView.as_view(), name='beneficiario_list'),
    path('beneficiario/crear/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('beneficiario/editar/<int:pk>/', BeneficiarioUpdateView.as_view(), name='beneficiario_update'),
    path('beneficiario/eliminar/<int:pk>/', BeneficiarioDeleteView.as_view(), name='beneficiario_delete'),
]
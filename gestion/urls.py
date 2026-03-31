from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario_list'),

    path('crear/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_delete'),

    path('moneda/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/crear/', MonedaCreateView.as_view(), name='moneda_create'),
    path('moneda/editar/<int:pk>/', MonedaUpdateView.as_view(), name='moneda_update'),
    path('moneda/eliminar/<int:pk>/', MonedaDeleteView.as_view(), name='moneda_delete'),

    path('transaccion/', TransaccionListView.as_view(), name='transaccion_list'),
    path('transaccion/crear/', TransaccionCreateView.as_view(), name='transaccion_create'),

    path('beneficiario/crear/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),

    path('deposito/', DepositoCreateView.as_view(), name='deposito_create'),

    path('cartola/<int:usuario_id>/', CartolaUsuarioView.as_view(), name='cartola_usuario'),
]
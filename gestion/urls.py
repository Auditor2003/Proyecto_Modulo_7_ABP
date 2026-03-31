from django.urls import path
from .views import *

urlpatterns = [
    path('', UsuarioListView.as_view(), name='usuario_list'),
    path('crear/', UsuarioCreateView.as_view(), name='usuario_create'),

    path('moneda/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/crear/', MonedaCreateView.as_view(), name='moneda_create'),

    path('transaccion/', TransaccionListView.as_view(), name='transaccion_list'),
    path('transaccion/crear/', TransaccionCreateView.as_view(), name='transaccion_create'),

    # Beneficiarios 
    path('beneficiario/', BeneficiarioListView.as_view(), name='beneficiario_list'),
    path('beneficiario/crear/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('beneficiario/editar/<int:pk>/', BeneficiarioUpdateView.as_view(), name='beneficiario_update'),
    path('beneficiario/eliminar/<int:pk>/', BeneficiarioDeleteView.as_view(), name='beneficiario_delete'),
]
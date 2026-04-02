from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),

    path('register/', views.register, name='register'),

    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/crear/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),

    path('monedas/', views.MonedaListView.as_view(), name='moneda_list'),
    path('monedas/crear/', views.MonedaCreateView.as_view(), name='moneda_create'),
    path('monedas/editar/<int:pk>/', views.MonedaUpdateView.as_view(), name='moneda_update'),
    path('monedas/eliminar/<int:pk>/', views.MonedaDeleteView.as_view(), name='moneda_delete'),

    path('beneficiarios/', views.BeneficiarioListView.as_view(), name='beneficiario_list'),
    path('beneficiarios/crear/', views.BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('beneficiarios/editar/<int:pk>/', views.BeneficiarioUpdateView.as_view(), name='beneficiario_update'),
    path('beneficiarios/eliminar/<int:pk>/', views.BeneficiarioDeleteView.as_view(), name='beneficiario_delete'),

    path('transacciones/', views.TransaccionListView.as_view(), name='transaccion_list'),
    path('transacciones/crear/', views.TransaccionCreateView.as_view(), name='transaccion_create'),

    path('deposito/', views.DepositoCreateView.as_view(), name='deposito_create'),

    path('cartola/<int:usuario_id>/', views.CartolaUsuarioView.as_view(), name='cartola_usuario'),
]
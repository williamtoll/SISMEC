from django.conf.urls import url
import apps.reportes.views as reportes_views

urlpatterns = [
    url(r'^sismec/reportes/estado_cuenta/$', reportes_views.estadoCuentacliente, name='estado_cuenta_cliente'),
    url(r'^sismec/reportes/productos_mas_vendidos/$', reportes_views.productosMasVendidos, name='productos_mas_vendidos'),
    url(r'^sismec/reportes/reporte_compras/$', reportes_views.movimientosCompras, name='movimientos_compras'),
    url(r'^sismec/reportes/reporte_ventas/$', reportes_views.movimientosVentas, name='movimientos_ventas'),
    url(r'^sismec/reportes/cuentas_a_pagar/$', reportes_views.cuentasAPagar, name='cuentas_a_pagar'),
    url(r'^sismec/reportes/ventas_mensuales/$', reportes_views.ventasPorMes, name='ventas_por_mes'),
]
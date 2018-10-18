from django.db import models

from apps.productos.models import Producto
from apps.proveedores.models import Proveedor

# Orden de Compra Cabecera
class OrdenCompraCab(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_pedido = models.DateField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, blank=True, null=True)
    PENDIENTE = 'PENDIENTE'
    CONFIRMADO = 'CONFIRMADO'
    FACTURADO = 'FACTURADO'
    RECHAZADO = 'RECHAZADO'
    ESTADO_CHOICES = (
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
        (FACTURADO, 'Facturado'),
        (RECHAZADO, 'Rechazado'),
    )
    estado = models.CharField(max_length=200)
    presupuesto_compra = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'orden_compra_cabecera'


# Orden de Compra Detalle
class OrdenCompraDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    compra_cab = models.ForeignKey(OrdenCompraCab, on_delete=models.PROTECT, blank=True, null= False)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null= False)
    cantidad = models.IntegerField(blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True,default=0)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'orden_compra_detalle'



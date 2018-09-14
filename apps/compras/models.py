from django.db import models

from apps.productos.models import Producto
from apps.proveedores.models import Proveedor


# Orden de Compra Cabecera
class OrdenCompraCab(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, blank=True, null=True)
    PENDIENTE = 'PENDIENTE'
    CONFIRMADO = 'CONFIRMADO'
    FACTURADO = 'FACTURADO'
    ESTADO_CHOICES = (
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
        (FACTURADO, 'Facturado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE)

    def __str__(self):
        return self.id

    def as_json(self):
        return dict(
            id=self.id)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'orden_compra_cabecera'


# Orden de Compra Detalle
class OrdenCompraDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    compra_cab = models.ForeignKey(OrdenCompraCab, on_delete=models.PROTECT, blank=True, null= False)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=False)
    cantidad = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id

    def as_json(self):
        return dict(
            id=self.id)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'orden_compra_detalle'

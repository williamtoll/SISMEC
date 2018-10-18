from django.db import models
from apps.clientes.models import Cliente
from apps.productos.models import Producto


# Presupuesto Venta Cabecera
class PresupuestoCab(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_presupesto = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, blank=True, null=True)

    PENDIENTE = 'PENDIENTE'
    CONFIRMADO = 'CONFIRMADO'
    FACTURADO = 'FACTURADO'
    ESTADO_CHOICES = (
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
        (FACTURADO, 'Facturado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE)
    monto_total = models.IntegerField(blank=True, null=True)
    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'presupuesto_cabecera'

# Presupuesto Detalle
class PresupuestoDet(models.Model):
    id = models.BigAutoField(primary_key=True)
    presupuesto_cab = models.ForeignKey(PresupuestoCab, on_delete=models.PROTECT, blank=True, null= False)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null= False)
    cantidad = models.IntegerField(blank=True, null=True)
    monto_unitario = models.IntegerField(blank=True, null=True)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'presupuesto_detalle'
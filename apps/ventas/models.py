from django.db import models
from apps.clientes.models import Cliente
from apps.productos.models import Producto


# Presupuesto Venta Cabecera
from apps.recepcion.models import RecepcionVehiculo


class PresupuestoCab(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_presupuesto = models.DateField(blank=True, null=True)
    recepcion_vehiculo = models.ForeignKey(RecepcionVehiculo,on_delete=models.PROTECT, blank=True, null=True )
    #monto_total = models.IntegerField(blank=True, null=True)
    motivo_anulacion = models.CharField(max_length=255, blank=True, null=True)
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
    precio_unitario = models.IntegerField(blank=True, null=True)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'presupuesto_detalle'
from django.db import models
from apps.clientes.models import Cliente
from apps.compras.models import OrdenCompraCab
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor

# Movimiento Cabecera
from apps.ventas.models import PresupuestoCab


class MovimientoCabecera(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_emision = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, blank=True, null=True)
    numero_factura = models.CharField(max_length=20, blank=True, null=False)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    nro_cuota = models.IntegerField(blank=True, null=True, default=0)
    COMPRA = 'COMPRA'
    VENTA = 'VENTA'
    MOVIMIENTO_CHOICES = (
        (COMPRA, 'Compra'),
        (VENTA, 'Venta'),
    )
    tipo_movimiento = models.CharField(max_length=20, choices=MOVIMIENTO_CHOICES, default=COMPRA)
    CONTADO = 'CONTADO'
    CREDITO = 'CREDITO'
    FACTURA_CHOICES = (
        (CONTADO, 'Contado'),
        (CREDITO, 'Credito'),
    )
    tipo_factura = models.CharField(max_length=20, choices=FACTURA_CHOICES, default=CONTADO)
    PENDIENTE = 'PENDIENTE'
    COBRADO = 'COBRADO'
    PAGADO = 'PAGADO'
    COMPLETADO = 'COMPLETADO'
    ANULADO ='ANULADO'
    CONDICION_CHOICES = (
        (PENDIENTE, 'Pendiente'),
        (COBRADO, 'Cobrado'),
        (PAGADO, 'Pagado'),
        (COMPLETADO, 'Completado'),
        (ANULADO, 'Anulado'),
    )
    estado = models.CharField(max_length=20, choices=CONDICION_CHOICES, default=COMPRA)
    monto_total = models.IntegerField(blank=True, null=True)
    grav10_total = models.IntegerField(blank=True, null=True)
    grav5_total = models.IntegerField(blank=True, null=True)
    iva10_total = models.IntegerField(blank=True, null=True)
    iva5_total = models.IntegerField(blank=True, null=True)
    timbrado = models.CharField(max_length=255)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    orden_compra = models.ForeignKey(OrdenCompraCab, on_delete=models.PROTECT, blank=True, null= True)
    presupuesto = models.ForeignKey(PresupuestoCab, on_delete=models.PROTECT, blank=True, null= True)
    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'movimiento_cabecera'


# Movimiento Detalle
class MovimientoDetalle(models.Model):
    id = models.BigAutoField(primary_key=True)
    movimiento_cab = models.ForeignKey(MovimientoCabecera, on_delete=models.PROTECT, blank=True, null= False)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null= False)
    cantidad = models.IntegerField(blank=True, null=True)
    precio_unitario = models.IntegerField(blank=True, null=True)
    exentas = models.IntegerField(blank=True, null=True)
    iva5 = models.IntegerField(blank=True, null=True)
    iva10 = models.IntegerField(blank=True, null=True)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'movimiento_detalle'

class CobroPagomodels(models.Model):
    id = models.BigAutoField(primary_key=True)
    movimiento_cab = models.ForeignKey(MovimientoCabecera, on_delete=models.PROTECT, blank=True, null=False)
    fecha = models.DateField(blank=True, null=True)
    nro_cuota = models.IntegerField(blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    nro_recibo = models.CharField(max_length=20, blank=True, null=False)
    forma_pago = models.CharField(max_length=20, blank=True, null=False)
    COBRO = 'COBRO'
    PAGO = 'PAGO'
    TIPO_CHOICES = (
        (COBRO, 'Cobro'),
        (PAGO, 'Pago'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=COBRO)
    ACTIVO = 'ACTIVO'
    ANULADO = 'ANULADO'
    ESTADO_CHOICES = (
        (ACTIVO, 'Activo'),
        (ANULADO, 'Anulado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ACTIVO)
    dato_adicional = models.CharField(max_length=200, blank=True, null=False)
    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'cobro_pago'
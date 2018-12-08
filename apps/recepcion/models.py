from django.db import models

from apps.clientes.models import Cliente

class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'marca'

class Modelo(models.Model):
    id = models.BigAutoField(primary_key=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, blank=True, null= False)
    descripcion = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.descripcion

    def __unicode__(self):
        return self.descripcion

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'modelo'

class RecepcionVehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, blank=True, null= False)
    fecha_recepcion = models.DateField(blank=True, null=False)
    chapa = models.CharField(max_length=255)
    kilometraje = models.IntegerField(blank=True, null=True)
    pertencencias_vehiculo = models.CharField(max_length=255)
    combustible_aprox = models.CharField(max_length=255)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, blank=True, null=False)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, blank=True, null=False)
    año = models.IntegerField(blank=True, null=True)
    detalle_problema = models.CharField(max_length=255)
    codigo_recepcion = models.CharField(max_length=255,  null=False, default="")
    RECIBIDO = 'RECIBIDO'
    PRESUPUESTADO = 'PRESUPUESTADO'
    RECHAZADO = 'RECHAZADO'
    APROBADO = 'APROBADO'
    FACTURADO = 'FACTURADO'
    PENDIENTEDEPAGO = 'PENDIENTE DE PAGO'
    PAGADO = 'PAGADO'
    ESTADO_CHOICES = (
        (RECIBIDO, 'Recibido'),
        (PRESUPUESTADO, 'Presupuestado'),
        (RECHAZADO, 'Rechazado'),
        (APROBADO, 'Aprobado'),
        (FACTURADO, 'Facturado'),
        (PENDIENTEDEPAGO, 'Pendiente de Pago'),
        (PAGADO, 'Pagado'),

    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=RECIBIDO)
    def __str__(self):
        return self.codigo_recepcion

    def as_json(self):
        return dict(
            label=self.codigo_recepcion,
            fecha_recepcion=self.fecha_recepcion,
            id=self.id)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'recepcion_vehiculo'


class SecuenciaNumerica(models.Model):
    ultimo_numero = models.IntegerField(blank=True, null=True)
    anho = models.IntegerField(blank=True, null=True)


    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'secuencia_numerica'
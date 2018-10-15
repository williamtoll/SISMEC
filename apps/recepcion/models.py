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
        db_table = 'descripcion'

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
    
    def __str__(self):
        return self.id

    def as_json(self):
        return dict(
            id=self.id)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'recepcion_vehiculo'
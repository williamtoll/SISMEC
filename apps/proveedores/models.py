from django.db import models


class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=255)
    ruc = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, blank=True)
    mail = models.CharField(max_length=255)

    def __str__(self):
        return self.nombres

    def as_json(self):
        return dict(
            label=self.nombres,
            cedula=self.ruc,
            id=self.id)

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'proveedor'

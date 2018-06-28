from django.db import models

#
class TipoProducto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=False)
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'producto_tipo'

class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_categoria = models.TextField(blank=False)
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_categoria

    def __unicode__(self):
        return self.nombre_categoria

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'categoria'

class UnidadMedida(models.Model):
    id = models.BigAutoField(primary_key=True)
    unidad_medida = models.TextField(blank=False)
    equivalencia = models.TextField(blank=False)
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unidad_medida

    def __unicode__(self):
        return self.unidad_medida

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'unidad_de_medida'

class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=False)
    descripcion = models.CharField(max_length=200, blank=False)
    marca = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio_venta = models.IntegerField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True)
    unidad_de_medida = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.BooleanField(default=False)
    provedor = models.CharField(max_length=20, blank=True) #Crear Clase Proveedor
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, blank=True, null=True)
    tipo_mpuesto = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre

    class Meta:
        """Establece las configuraciones del modelo de base de datos"""
        managed = True
        db_table = 'producto'


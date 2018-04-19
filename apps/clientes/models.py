from django.db import models


class Cliente(models.Model):
    cedula = models.CharField(unique=True, max_length=10, blank=False, null=False)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField('fecha de nacimiento')
    ruc = models.CharField(max_length=255)
    SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Femenino"),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    direccion_particular = models.CharField(max_length=255)
    telefono_particular = models.CharField(max_length=255, blank=True)
    celular = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    contactoAux = models.CharField('Contacto Auxiliar', max_length=255, blank=True)
    telefonoAux = models.CharField('Contacto Auxiliar',max_length=255, blank=True)
    deuda_contraida = models.BigIntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(u'%s %s' % (self.nombres, self.apellidos))

    def as_json(self):
        return dict(
            label=self.nombres + ' ' + self.apellidos,
            cedula=self.cedula,
            id=self.id)

    class Meta:
        permissions = (
            ('ver_listado_clientes', 'Ver listado de clientes'),
            ('ver_opciones_cliente', 'Ver opciones de clientes'),
        )

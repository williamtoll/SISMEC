# Generated by Django 2.0.4 on 2018-10-16 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
                ('marca', models.CharField(blank=True, max_length=200)),
                ('cantidad', models.IntegerField(blank=True, default=0)),
                ('precio_venta', models.IntegerField(blank=True, null=True)),
                ('estado', models.BooleanField(default=False)),
                ('tipo_impuesto', models.CharField(choices=[('EXENTAS', 'Exentas'), ('IVA10', 'Iva 10'), ('IVA5', 'Iva 5')], default='IVA10', max_length=20)),
            ],
            options={
                'managed': True,
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha_hora_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'managed': True,
                'db_table': 'producto_tipo',
            },
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('unidad_medida', models.CharField(max_length=200)),
                ('equivalencia', models.CharField(max_length=200)),
                ('fecha_hora_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'managed': True,
                'db_table': 'unidad_de_medida',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='productos.TipoProducto'),
        ),
    ]

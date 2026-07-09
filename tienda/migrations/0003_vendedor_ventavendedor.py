from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_producto_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id_vendedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=15, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'vendedor'},
        ),
        migrations.CreateModel(
            name='VentaVendedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_venta', models.OneToOneField(
                    db_column='id_venta',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='info_vendedor',
                    to='tienda.venta',
                )),
                ('id_vendedor', models.ForeignKey(
                    blank=True,
                    db_column='id_vendedor',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='ventas',
                    to='tienda.vendedor',
                )),
                ('id_cliente', models.IntegerField(blank=True, null=True)),
                ('nombre_cliente', models.CharField(blank=True, max_length=200, null=True)),
                ('neto', models.IntegerField(default=0)),
                ('comision', models.IntegerField(default=0)),
            ],
            options={'db_table': 'venta_vendedor'},
        ),
    ]

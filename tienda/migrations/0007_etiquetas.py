from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0006_venta_origen'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionEtiqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_papel', models.CharField(
                    choices=[
                        ('carta', 'Carta (216×279 mm)'),
                        ('a4', 'A4 (210×297 mm)'),
                        ('oficio', 'Oficio (216×330 mm)'),
                        ('personalizado', 'Personalizado'),
                    ],
                    default='carta', max_length=15,
                )),
                ('ancho_mm', models.DecimalField(decimal_places=2, default=216, max_digits=7)),
                ('alto_mm', models.DecimalField(decimal_places=2, default=279, max_digits=7)),
                ('orientacion', models.CharField(
                    choices=[('portrait', 'Vertical'), ('landscape', 'Horizontal')],
                    default='portrait', max_length=10,
                )),
            ],
            options={'db_table': 'configuracion_etiqueta'},
        ),
        migrations.CreateModel(
            name='EtiquetaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_delantera', models.FileField(blank=True, null=True, upload_to='etiquetas/')),
                ('archivo_especificaciones', models.FileField(blank=True, null=True, upload_to='etiquetas/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('producto', models.OneToOneField(
                    db_column='id_producto',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='etiqueta',
                    to='tienda.producto',
                )),
            ],
            options={'db_table': 'etiqueta_producto'},
        ),
    ]

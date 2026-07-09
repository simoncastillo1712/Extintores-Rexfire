from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_conversacionwhatsapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversacionEstado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=30, unique=True)),
                ('estado', models.CharField(
                    choices=[
                        ('en_consulta',        'En consulta'),
                        ('interesado',         'Interesado'),
                        ('cotizacion_enviada', 'Cotización enviada'),
                        ('concretada',         'Compra concretada'),
                        ('abandonada',         'Abandonó el carrito'),
                    ],
                    default='en_consulta',
                    max_length=25,
                )),
                ('notas', models.TextField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'conversacion_estado'},
        ),
    ]

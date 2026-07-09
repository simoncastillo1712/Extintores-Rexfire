from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_vendedor_ventavendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversacionWhatsapp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=30)),
                ('rol', models.CharField(max_length=10)),
                ('contenido', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'conversacion_whatsapp',
                'ordering': ['fecha'],
            },
        ),
    ]

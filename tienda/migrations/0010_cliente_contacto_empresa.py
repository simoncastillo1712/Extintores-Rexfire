from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0009_seguimiento_cliente'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE cliente ADD COLUMN contacto_empresa VARCHAR(100) NULL DEFAULT NULL;",
            reverse_sql="ALTER TABLE cliente DROP COLUMN contacto_empresa;",
            state_operations=[
                migrations.AddField(
                    model_name='cliente',
                    name='contacto_empresa',
                    field=models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
    ]

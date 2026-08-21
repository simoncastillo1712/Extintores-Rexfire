from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0007_etiquetas'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE cliente ADD COLUMN fecha_ultimo_trabajo DATE NULL DEFAULT NULL;",
            reverse_sql="ALTER TABLE cliente DROP COLUMN fecha_ultimo_trabajo;",
            state_operations=[
                migrations.AddField(
                    model_name='cliente',
                    name='fecha_ultimo_trabajo',
                    field=models.DateField(blank=True, null=True),
                ),
            ],
        ),
    ]

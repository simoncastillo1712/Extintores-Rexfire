import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0010_cliente_contacto_empresa'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE venta "
                "ADD COLUMN estado VARCHAR(12) NOT NULL DEFAULT 'confirmada', "
                "ADD COLUMN id_cliente INT NULL DEFAULT NULL, "
                "ADD COLUMN id_vendedor INT NULL DEFAULT NULL;"
            ),
            reverse_sql=(
                "ALTER TABLE venta "
                "DROP COLUMN estado, "
                "DROP COLUMN id_cliente, "
                "DROP COLUMN id_vendedor;"
            ),
            state_operations=[
                migrations.AddField(
                    model_name='venta',
                    name='estado',
                    field=models.CharField(
                        choices=[('cotizacion', 'Cotización pendiente'), ('confirmada', 'Venta confirmada')],
                        default='confirmada', max_length=12,
                    ),
                ),
                migrations.AddField(
                    model_name='venta',
                    name='id_cliente',
                    field=models.ForeignKey(
                        blank=True, null=True, db_column='id_cliente', db_constraint=False,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='ventas_pendientes', to='tienda.cliente',
                    ),
                ),
                migrations.AddField(
                    model_name='venta',
                    name='id_vendedor',
                    field=models.ForeignKey(
                        blank=True, null=True, db_column='id_vendedor', db_constraint=False,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='ventas_pendientes', to='tienda.vendedor',
                    ),
                ),
            ],
        ),
    ]

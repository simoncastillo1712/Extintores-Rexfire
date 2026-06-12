from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_conversacionestado'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE venta ADD COLUMN origen VARCHAR(10) NULL DEFAULT 'web';",
            reverse_sql="ALTER TABLE venta DROP COLUMN origen;",
        ),
    ]

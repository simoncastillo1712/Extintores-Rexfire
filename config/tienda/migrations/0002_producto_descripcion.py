from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE producto ADD COLUMN descripcion TEXT NULL;",
            reverse_sql="ALTER TABLE producto DROP COLUMN descripcion;",
        ),
    ]

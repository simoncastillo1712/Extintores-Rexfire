from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_conversacionestado'),
    ]

    operations = [
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

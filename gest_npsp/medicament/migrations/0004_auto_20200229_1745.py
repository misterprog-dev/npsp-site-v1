# Generated by Django 3.0 on 2020-02-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicament', '0003_auto_20200229_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicament',
            name='kilo_paquet',
            field=models.DecimalField(decimal_places=10, default=1.0, max_digits=15),
        ),
    ]

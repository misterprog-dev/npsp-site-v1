# Generated by Django 3.0 on 2020-02-29 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0005_auto_20200229_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='password',
            field=models.CharField(default='uDUHqXRmFl', help_text='Mot de passe par defaut : uDUHqXRmFl', max_length=50),
        ),
        migrations.AlterField(
            model_name='gestionnaire',
            name='password',
            field=models.CharField(default='1eqC9dOP3e', help_text='Mot de passe definit', max_length=50),
        ),
    ]

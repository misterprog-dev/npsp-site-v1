# Generated by Django 3.0 on 2020-02-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0004_auto_20200229_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='password',
            field=models.CharField(default='v7pSk8wJec', help_text='Mot de passe par defaut : v7pSk8wJec', max_length=50),
        ),
        migrations.AlterField(
            model_name='gestionnaire',
            name='password',
            field=models.CharField(default='lxitz1Cf9m', help_text='Mot de passe definit', max_length=50),
        ),
    ]

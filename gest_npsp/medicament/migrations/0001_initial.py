# Generated by Django 3.0 on 2020-02-23 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TypeMedicament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=300, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_produit', models.CharField(max_length=300, unique=True)),
                ('libelle_produit', models.CharField(max_length=300)),
                ('dosage', models.IntegerField()),
                ('unite', models.CharField(choices=[('g', 'gramme'), ('mg', 'milligramme')], max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type_medicament', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='medicament.TypeMedicament')),
            ],
            options={
                'unique_together': {('code_produit',)},
            },
        ),
    ]

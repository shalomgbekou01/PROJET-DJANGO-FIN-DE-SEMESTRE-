# Generated by Django 5.1.5 on 2025-02-24 02:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartShop', '0013_remove_vente_client_vente_adresse_vente_datevente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='client',
            field=models.ForeignKey(default=50, on_delete=django.db.models.deletion.CASCADE, to='SmartShop.client'),
        ),
    ]

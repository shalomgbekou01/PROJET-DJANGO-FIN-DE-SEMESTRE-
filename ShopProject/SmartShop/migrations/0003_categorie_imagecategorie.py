# Generated by Django 5.1.5 on 2025-02-05 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartShop', '0002_alter_produit_imageproduit'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='imageCategorie',
            field=models.ImageField(default='default.png', upload_to='categories/'),
        ),
    ]

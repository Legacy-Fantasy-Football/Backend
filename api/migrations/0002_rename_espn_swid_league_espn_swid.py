# Generated by Django 4.0.6 on 2022-07-23 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='league',
            old_name='Espn_SWID',
            new_name='Espn_Swid',
        ),
    ]

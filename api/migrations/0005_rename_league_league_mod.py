# Generated by Django 4.0.1 on 2022-07-25 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_leaguemodel_league'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='League',
            new_name='League_Mod',
        ),
    ]
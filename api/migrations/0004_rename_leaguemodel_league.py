# Generated by Django 4.0.1 on 2022-07-25 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_leaguemodel_delete_league'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeagueModel',
            new_name='League',
        ),
    ]
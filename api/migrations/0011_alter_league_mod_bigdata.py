# Generated by Django 4.0.1 on 2022-07-26 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_league_mod_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league_mod',
            name='bigdata',
            field=models.JSONField(default=dict, null=True),
        ),
    ]

# Generated by Django 4.0.1 on 2022-07-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_league_mod_bigdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league_mod',
            name='bigdata',
            field=models.JSONField(default=list, null=True),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-07 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0002_alter_spacestation_date_broken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacestation',
            name='condition',
            field=models.CharField(choices=[('running', 'running'), ('broken', 'broken')], default='running', max_length=8),
        ),
    ]

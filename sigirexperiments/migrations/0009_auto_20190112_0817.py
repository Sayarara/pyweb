# Generated by Django 2.1.3 on 2019-01-12 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sigirexperiments', '0008_patternseedtemp_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patternseedtemp',
            name='seedsubstring',
            field=models.TextField(),
        ),
    ]

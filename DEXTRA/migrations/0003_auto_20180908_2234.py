# Generated by Django 2.1.1 on 2018-09-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DEXTRA', '0002_auto_20180908_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='coraattrvalue',
            name='userid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coravaluesynonym',
            name='userid',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 2.1.1 on 2018-09-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERtasks', '0004_clustercora'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustercora',
            name='is_checked',
            field=models.IntegerField(default=-1),
        ),
    ]

# Generated by Django 2.1.1 on 2018-09-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=128)),
                ('pwd', models.CharField(max_length=128)),
                ('domain', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=128)),
                ('hobby', models.CharField(max_length=128)),
            ],
        ),
    ]

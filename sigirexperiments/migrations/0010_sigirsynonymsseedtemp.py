# Generated by Django 2.1.3 on 2019-01-13 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sigirexperiments', '0009_auto_20190112_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='sigirSynonymsSeedTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='aming', max_length=128)),
                ('cattr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sigirexperiments.sigirCoraAttr')),
            ],
        ),
    ]

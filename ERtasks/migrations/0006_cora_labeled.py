# Generated by Django 2.1.3 on 2019-01-06 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERtasks', '0005_clustercora_is_checked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cora_labeled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entityurl', models.CharField(max_length=128)),
                ('text', models.TextField()),
                ('labeledtext', models.TextField(default=models.TextField())),
            ],
        ),
    ]

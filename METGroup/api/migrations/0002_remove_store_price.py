# Generated by Django 3.2.4 on 2021-12-22 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='price',
        ),
    ]

# Generated by Django 3.0 on 2022-03-07 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rferog', '0002_auto_20220307_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='topic',
        ),
    ]
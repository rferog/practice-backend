# Generated by Django 3.0 on 2022-03-01 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField()),
                ('topic', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('commentsNumber', models.IntegerField()),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.IntegerField()),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rferog.Post')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]

# Generated by Django 3.0.5 on 2021-07-29 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201205_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prf_ProfileImg',
            field=models.ImageField(blank=True, max_length=250, null=True, upload_to='', verbose_name='Profile image'),
        ),
    ]

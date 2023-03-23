# Generated by Django 3.0.5 on 2020-11-27 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_auto_20201123_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tekst',
            name='tks_Categories',
        ),
        migrations.AddField(
            model_name='profile',
            name='prf_User',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

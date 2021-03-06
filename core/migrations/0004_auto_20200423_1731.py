# Generated by Django 3.0.5 on 2020-04-23 17:31

import core.fields
from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200423_1248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagegenre',
            options={'verbose_name_plural': 'imagegenres'},
        ),
        migrations.AlterModelOptions(
            name='textgenre',
            options={'verbose_name_plural': 'textgenres'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.AlterField(
            model_name='imagegenre',
            name='ign_Slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('ign_Title',)),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=core.fields.ImageThumbsField(blank=True, max_length=250, null=True, sizes=({'code': 'thumb', 'resize': 'crop', 'wxh': '100x72'}, {'code': 'galry', 'resize': 'crop', 'wxh': '250x180'}, {'code': 'detail', 'wxh': '800x576'}), upload_to=''),
        ),
        migrations.AlterField(
            model_name='textgenre',
            name='tgn_Slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('tgn_Title',)),
        ),
    ]

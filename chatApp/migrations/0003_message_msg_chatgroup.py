# Generated by Django 3.0.5 on 2021-08-01 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatApp', '0002_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='msg_ChatGroup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='chatApp.Chat'),
            preserve_default=False,
        ),
    ]

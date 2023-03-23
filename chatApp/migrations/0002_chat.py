# Generated by Django 3.0.5 on 2021-07-31 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_profile_prf_profileimg'),
        ('chatApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cht_Name', models.CharField(default='chat', max_length=85, verbose_name='Naam van chat')),
                ('cht_Ctrl', models.TextField(verbose_name='Control field')),
                ('cht_Gen', models.DateTimeField(auto_now_add=True, verbose_name='moment van creatie')),
                ('cht_Notes', models.TextField(verbose_name='Notes and info')),
                ('cht_Type', models.CharField(blank=True, choices=[('D', 'Dialog'), ('G', 'Group')], default='D', help_text='Groeps chat of dialoog', max_length=1, null=True, verbose_name='Type Chat')),
                ('cht_Contacts', models.ManyToManyField(related_name='chatContacts', related_query_name='chtContQry', to='core.Profile')),
            ],
        ),
    ]
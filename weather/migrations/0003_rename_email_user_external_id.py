# Generated by Django 3.2 on 2021-04-19 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_auto_20210416_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='external_id',
        ),
    ]

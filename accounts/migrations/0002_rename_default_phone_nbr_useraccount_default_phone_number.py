# Generated by Django 3.2 on 2022-05-24 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='default_phone_number',
            new_name='default_phone_number',
        ),
    ]

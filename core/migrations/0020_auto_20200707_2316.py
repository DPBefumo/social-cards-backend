# Generated by Django 3.0.7 on 2020-07-07 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200707_1810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='time_stamp',
            new_name='posted_at',
        ),
    ]

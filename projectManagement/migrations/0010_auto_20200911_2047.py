# Generated by Django 3.0.7 on 2020-09-11 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0009_auto_20200911_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='status',
            new_name='ok',
        ),
    ]

# Generated by Django 3.0.7 on 2020-08-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='path',
        ),
        migrations.AddField(
            model_name='video',
            name='docFile',
            field=models.FileField(default=None, upload_to='videos/%Y/%m/%d'),
        ),
    ]

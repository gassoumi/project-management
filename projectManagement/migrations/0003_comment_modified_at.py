# Generated by Django 3.0.7 on 2020-09-03 06:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0002_auto_20200825_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 3, 6, 0, 40, 976959, tzinfo=utc)),
        ),
    ]

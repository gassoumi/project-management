# Generated by Django 3.0.7 on 2020-09-25 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectManagement', '0017_auto_20200925_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='status',
            field=models.CharField(choices=[('CLOTURE', 'cloturé'), ('NON_CLOTURE', 'non cloturé')], default='NON_CLOTURE', max_length=50),
        ),
    ]

# Generated by Django 2.0 on 2018-03-31 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_auto_20180331_0307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingresso',
            name='assento',
        ),
    ]

# Generated by Django 2.1.7 on 2024-06-24 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CQM', '0012_cqm_r1s'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cqmproject',
            name='Customer',
            field=models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(NB)-SMB', 'C38(NB)-SMB'), ('C38(AIO)', 'C38(AIO)'), ('T88(AIO)', 'T88(AIO)'), ('T89(NB)', 'T89(NB)'), ('A39', 'A39'), ('C85', 'C85'), ('Others', 'Others')], max_length=20, verbose_name='Customer'),
        ),
    ]

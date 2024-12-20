# Generated by Django 2.1.7 on 2020-12-23 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QIL', '0002_auto_20200731_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qil_m',
            name='Customer',
            field=models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(AIO)', 'C38(AIO)'), ('T88(AIO)', 'T88(AIO)'), ('A39', 'A39'), ('Others', 'Others')], max_length=20, verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='qil_m',
            name='Status',
            field=models.CharField(choices=[('', ''), ('Closed', 'Closed'), ('Deleted', 'Deleted'), ('In Process', 'In Process'), ('Lesson Learn', 'Lesson Learn'), ('Open', 'Open')], max_length=100, verbose_name='Status'),
        ),
    ]

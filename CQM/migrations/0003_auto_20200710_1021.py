# Generated by Django 2.1.7 on 2020-07-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CQM', '0002_auto_20200709_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cqm',
            name='R1_PN_Description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='R1_PN_Description'),
        ),
    ]

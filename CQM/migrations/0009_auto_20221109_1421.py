# Generated by Django 2.1.7 on 2022-11-09 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CQM', '0008_auto_20220126_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cqm',
            name='Comments',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Comments'),
        ),
    ]

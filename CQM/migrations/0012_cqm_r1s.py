# Generated by Django 2.1.7 on 2023-06-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CQM', '0011_auto_20230109_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='cqm',
            name='R1S',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='R1S'),
        ),
    ]

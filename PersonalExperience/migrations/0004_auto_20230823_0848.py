# Generated by Django 2.1.7 on 2023-08-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalExperience', '0003_perexperience_dalei'),
    ]

    operations = [
        migrations.AddField(
            model_name='perexperience',
            name='Item',
            field=models.CharField(default='', max_length=20, verbose_name='职称项次'),
        ),
        migrations.AddField(
            model_name='perexperience',
            name='Positions_Name',
            field=models.CharField(default='', max_length=20, verbose_name='职称'),
        ),
    ]

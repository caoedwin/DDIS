# Generated by Django 2.1.7 on 2025-07-11 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0040_auto_20250711_1111'),
        ('CommonFiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonfiles',
            name='Creator',
            field=models.CharField(default='', max_length=50, verbose_name='Creator'),
        ),
        migrations.RemoveField(
            model_name='commonfiles',
            name='Owner',
        ),
        migrations.AddField(
            model_name='commonfiles',
            name='Owner',
            field=models.ManyToManyField(to='app01.UserInfo'),
        ),
    ]

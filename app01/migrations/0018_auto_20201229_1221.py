# Generated by Django 2.1.7 on 2020-12-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0017_auto_20201223_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinfoindct',
            name='CPU',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='CPU'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='DQAPL',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='DQAPL'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='LD',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='LD'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='ModifiedDate',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='ModifiedDate'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='OSSupport',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='OSSupport'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='Platform',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Platform'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='PrjEngCode1',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='PrjEngCode1'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='PrjEngCode2',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='PrjEngCode2'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='ProjectName',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='ProjectName'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='SS',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='SS'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='Size',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='projectinfoindct',
            name='VGA',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='VGA'),
        ),
    ]
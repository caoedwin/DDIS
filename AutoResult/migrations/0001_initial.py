# Generated by Django 2.1.7 on 2022-01-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app01', '0019_auto_20210928_1432'),
        ('CQM', '0007_auto_20210422_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=64, unique=True, verbose_name='No.')),
                ('Customer', models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(AIO)', 'C38(AIO)'), ('T88(AIO)', 'T88(AIO)'), ('C85', 'C85'), ('A39', 'A39'), ('Common', 'Common'), ('網絡', '網絡')], max_length=64, verbose_name='CG')),
                ('ValueIf', models.CharField(choices=[('N-VA', 'N-VA'), ('VA', 'VA')], max_length=64, verbose_name='VA/N-VA')),
                ('BaseIncome', models.CharField(blank=True, max_length=64, null=True, verbose_name='Base效益')),
                ('CaseID', models.CharField(blank=True, max_length=64, null=True, verbose_name='Case ID')),
                ('CaseName', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Case Name')),
                ('Item', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item')),
                ('Status', models.CharField(choices=[('V', 'V'), ('X', 'X')], default='', max_length=50, verbose_name='Status')),
                ('Owner', models.CharField(blank=True, max_length=50, null=True, verbose_name='Owner')),
                ('FunDescription', models.CharField(blank=True, max_length=1000, null=True, verbose_name='功能簡介')),
                ('Comment', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'AutoItems',
                'verbose_name_plural': 'AutoItems',
            },
        ),
        migrations.CreateModel(
            name='AutoProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer', models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(NB)-SMB', 'C38(NB)-SMB'), ('C38(AIO)', 'C38(AIO)'), ('T88(AIO)', 'T88(AIO)'), ('A39', 'A39'), ('C85', 'C85'), ('Others', 'Others')], max_length=20, verbose_name='Customer')),
                ('Project', models.CharField(max_length=20, unique=True, verbose_name='Project')),
                ('Year', models.CharField(default='', max_length=20, verbose_name='SS年份')),
                ('Owner', models.ManyToManyField(to='app01.UserInfo')),
            ],
            options={
                'verbose_name': 'AutoProject',
                'verbose_name_plural': 'AutoProject',
            },
        ),
        migrations.CreateModel(
            name='AutoResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=64, verbose_name='No.')),
                ('Customer', models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(AIO)', 'C38(AIO)'), ('T88(AIO)', 'T88(AIO)'), ('C85', 'C85'), ('A39', 'A39'), ('Common', 'Common'), ('網絡', '網絡')], max_length=64, verbose_name='CG')),
                ('ValueIf', models.CharField(choices=[('N-VA', 'N-VA'), ('VA', 'VA')], max_length=64, verbose_name='VA/N-VA')),
                ('BaseIncome', models.CharField(blank=True, max_length=64, null=True, verbose_name='Base效益')),
                ('CaseID', models.CharField(blank=True, max_length=64, null=True, verbose_name='Case ID')),
                ('CaseName', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Case Name')),
                ('Item', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item')),
                ('Status', models.CharField(choices=[('V', 'V'), ('X', 'X')], default='', max_length=50, verbose_name='Status')),
                ('Owner', models.CharField(blank=True, max_length=50, null=True, verbose_name='Owner')),
                ('FunDescription', models.CharField(blank=True, max_length=1000, null=True, verbose_name='功能簡介')),
                ('Comment', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comment')),
                ('ProjectName', models.CharField(blank=True, max_length=50, null=True, verbose_name='ProjectName')),
                ('Year', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='SS年份')),
                ('Cycles', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cycles')),
                ('Comments', models.CharField(blank=True, max_length=5000, null=True, verbose_name='Comments')),
                ('editor', models.CharField(max_length=100, verbose_name='editor')),
                ('edit_time', models.CharField(max_length=26, verbose_name='edit_time')),
                ('AutoItem', models.ForeignKey(blank=True, null=True, on_delete=True, to='AutoResult.AutoItems')),
                ('Projectinfo', models.ForeignKey(blank=True, null=True, on_delete=True, to='AutoResult.AutoProject')),
                ('ProjectinfoCQM', models.ForeignKey(blank=True, null=True, on_delete=True, to='CQM.CQMProject')),
            ],
        ),
        migrations.CreateModel(
            name='PICS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='Adapter/PIC/', verbose_name='图片地址')),
                ('single', models.CharField(blank=True, max_length=200, null=True, verbose_name='图片名称')),
            ],
        ),
    ]

# Generated by Django 2.1.7 on 2023-03-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0024_auto_20230227_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='department',
            field=models.IntegerField(choices=[(1, '测试部门'), (3, 'PM'), (4, '其它部门'), (2, '开发部门')], default=1, verbose_name='部门'),
        ),
    ]
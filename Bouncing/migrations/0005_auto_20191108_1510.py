# Generated by Django 2.1.7 on 2019-11-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bouncing', '0004_bouncing_m_a_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='files_BM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, null=True, upload_to='files_B/', verbose_name='文件内容')),
                ('single', models.CharField(blank=True, max_length=100, null=True, verbose_name='文件名称')),
            ],
        ),
        migrations.AddField(
            model_name='bouncing_m',
            name='files_B',
            field=models.ManyToManyField(blank=True, related_name='files_B', to='Bouncing.files_BM', verbose_name='图文件表'),
        ),
    ]
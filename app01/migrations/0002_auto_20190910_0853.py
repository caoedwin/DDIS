# Generated by Django 2.1.7 on 2019-09-10 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson_learn',
            name='Photo',
            field=models.ManyToManyField(blank=True, related_name='imgs', to='app01.Imgs', verbose_name='图片表'),
        ),
        migrations.AlterField(
            model_name='lesson_learn',
            name='video',
            field=models.ManyToManyField(blank=True, related_name='video', to='app01.files', verbose_name='视频表'),
        ),
    ]

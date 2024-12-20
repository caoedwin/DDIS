# Generated by Django 2.1.7 on 2020-04-10 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app01', '0010_auto_20200325_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='lessonlearn_Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('', ''), ('Pass', 'Pass'), ('Fail', 'Fail'), ('N/S', 'N/S'), ('N/A', 'N/A')], max_length=20)),
                ('Comment', models.CharField(max_length=1000)),
                ('editor', models.CharField(default='', max_length=100)),
                ('edit_time', models.CharField(blank=True, default='', max_length=26, verbose_name='edit_time')),
            ],
        ),
        migrations.CreateModel(
            name='TestProjectLL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer', models.CharField(choices=[('', ''), ('C38(NB)', 'C38(NB)'), ('C38(NB)-SMB', 'C38(NB)-SMB'), ('C38(AIO)', 'C38(AIO)'), ('A39', 'A39'), ('Others', 'Others')], max_length=20, verbose_name='Customer')),
                ('Project', models.CharField(max_length=20, verbose_name='Project')),
                ('Owner', models.ManyToManyField(to='app01.UserInfo')),
            ],
            options={
                'verbose_name': 'TestProjectLL',
                'verbose_name_plural': 'TestProjectLL',
            },
        ),
        migrations.AddField(
            model_name='lessonlearn_project',
            name='Projectinfo',
            field=models.ForeignKey(on_delete=True, to='LessonProjectME.TestProjectLL'),
        ),
        migrations.AddField(
            model_name='lessonlearn_project',
            name='lesson',
            field=models.ForeignKey(on_delete=True, to='app01.lesson_learn'),
        ),
    ]

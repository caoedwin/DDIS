# Generated by Django 2.1.7 on 2020-10-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LessonProjectME', '0002_auto_20200806_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonlearn_project',
            name='result',
            field=models.CharField(choices=[('', ''), ('Pass', 'Pass'), ('Fail', 'Fail'), ('N/S', 'N/S'), ('N/A', 'N/A'), ('N/P', 'N/P')], max_length=20),
        ),
    ]
# Generated by Django 2.1.7 on 2019-12-16 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DriverList_M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer', models.CharField(max_length=20)),
                ('Project', models.CharField(max_length=20)),
                ('Phase0', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=400)),
                ('Function', models.CharField(blank=True, max_length=50, null=True)),
                ('Vendor', models.CharField(blank=True, max_length=150, null=True)),
                ('Version', models.CharField(max_length=150)),
                ('Image', models.CharField(max_length=50)),
                ('Driver', models.CharField(max_length=50)),
                ('editor', models.CharField(blank=True, max_length=20, null=True)),
                ('edit_time', models.CharField(blank=True, max_length=26, null=True, verbose_name='edit_time')),
            ],
        ),
        migrations.CreateModel(
            name='ToolList_M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer', models.CharField(max_length=20)),
                ('Project', models.CharField(max_length=20)),
                ('Phase0', models.CharField(max_length=20)),
                ('Vendor', models.CharField(blank=True, max_length=150, null=True)),
                ('Version', models.CharField(max_length=150)),
                ('ToolName', models.CharField(max_length=300)),
                ('TestCase', models.CharField(blank=True, max_length=100, null=True)),
                ('editor', models.CharField(blank=True, max_length=20, null=True)),
                ('edit_time', models.CharField(blank=True, max_length=26, null=True, verbose_name='edit_time')),
            ],
        ),
    ]
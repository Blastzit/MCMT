# Generated by Django 5.1 on 2024-08-14 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]

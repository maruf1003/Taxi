# Generated by Django 3.2.13 on 2022-04-14 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0011_auto_20220414_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tellmetype',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]

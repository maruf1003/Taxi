# Generated by Django 3.2.1 on 2022-04-01 12:10

from django.db import migrations, models
import taxi.models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0003_customuser_sms_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='users/default.png', null=True, upload_to=taxi.models.get_avatar),
        ),
        migrations.AddField(
            model_name='customuser',
            name='car_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='car_number',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='complete',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='langtude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='latitude',
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 3.2.13 on 2022-04-14 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drive', '0004_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='TellMe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=110, null=True)),
                ('desc', models.CharField(default='', max_length=200, null=True)),
                ('data_time', models.DateTimeField(default='', null=True)),
                ('place', models.CharField(default='', max_length=110, null=True)),
                ('accident', models.CharField(default='', max_length=110, null=True)),
                ('photo', models.ImageField(default='', null=True, upload_to='')),
                ('driver', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='drive.driver')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

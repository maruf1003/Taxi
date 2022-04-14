# Generated by Django 3.2.13 on 2022-04-14 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0015_tellme_tell_me_typ'),
    ]

    operations = [
        migrations.AddField(
            model_name='tellme',
            name='massage',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tellme',
            name='driver',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='drive.driver'),
        ),
    ]
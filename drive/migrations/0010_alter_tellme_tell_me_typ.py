# Generated by Django 3.2.13 on 2022-04-14 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0009_alter_tellme_tell_me_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tellme',
            name='tell_me_typ',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='drive.tellmetype'),
        ),
    ]
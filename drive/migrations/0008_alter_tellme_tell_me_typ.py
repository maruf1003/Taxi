# Generated by Django 3.2.13 on 2022-04-14 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0007_auto_20220414_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tellme',
            name='tell_me_typ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drive.tellmetype'),
        ),
    ]

# Generated by Django 2.1.2 on 2020-06-22 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0013_auto_20200622_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carset',
            name='build_num',
        ),
        migrations.RemoveField(
            model_name='carset',
            name='sela_staff',
        ),
        migrations.RemoveField(
            model_name='house',
            name='sela_staff',
        ),
        migrations.AddField(
            model_name='buildnum',
            name='is_car',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='house',
            name='set_type',
            field=models.IntegerField(choices=[(0, '子母'), (1, '标准')], default=1),
        ),
        migrations.DeleteModel(
            name='CarSet',
        ),
    ]
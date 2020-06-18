# Generated by Django 2.1.2 on 2020-06-17 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('info', models.TextField()),
                ('room_num', models.CharField(blank=True, max_length=20, null=True)),
                ('area', models.IntegerField(blank=True)),
                ('is_full_money', models.BooleanField(default=False)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.IntegerField(blank=True)),
                ('memo', models.TextField()),
                ('status', models.IntegerField(choices=[(0, '可售房源'), (1, '销控房源'), (2, '签约房源'), (3, '全款到账')], default=0)),
            ],
        ),
    ]

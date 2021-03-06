# Generated by Django 2.1.2 on 2020-06-20 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200617_1919'),
        ('house', '0009_house_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.IntegerField(choices=[(0, '可售房源'), (1, '销控房源'), (2, '签约房源'), (3, '全款到账')], default=0)),
                ('is_full_money', models.BooleanField(default=False)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('floor', models.IntegerField(blank=True, null=True)),
                ('set_type', models.IntegerField(choices=[(0, '子母'), (1, '标准')], default=1)),
                ('count', models.IntegerField(default=1)),
                ('set_num_1', models.CharField(blank=True, max_length=20, null=True)),
                ('set_num_2', models.CharField(blank=True, max_length=20, null=True)),
                ('sela_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Staff')),
            ],
        ),
    ]

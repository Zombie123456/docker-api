# Generated by Django 2.1.2 on 2020-06-22 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0012_auto_20200620_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('build_num', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='house.BuildNum')),
            ],
        ),
        migrations.AddField(
            model_name='carset',
            name='build_num',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='house.BuildNum'),
        ),
    ]
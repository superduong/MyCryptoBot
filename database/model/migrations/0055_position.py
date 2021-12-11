# Generated by Django 3.2 on 2021-12-11 18:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0054_alter_pipeline_strategy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_trading', models.BooleanField(blank=True, default=False, null=True)),
                ('buying_price', models.FloatField()),
                ('amount', models.FloatField()),
                ('open', models.BooleanField(blank=True, default=True)),
                ('open_time', models.DateTimeField(default=datetime.datetime(2021, 12, 11, 12, 27, 36, 748070))),
                ('close_time', models.DateTimeField(blank=True, null=True)),
                ('exchange', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='model.exchange')),
                ('symbol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='model.symbol')),
            ],
        ),
    ]
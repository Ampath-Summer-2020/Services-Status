# Generated by Django 3.0.5 on 2020-04-29 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0029_auto_20200429_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subservice',
            name='services',
        ),
        migrations.CreateModel(
            name='Topology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='status.Priority')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='status.Service', verbose_name='Service')),
                ('subservices', models.ManyToManyField(blank=True, to='status.SubService', verbose_name='Sub - Service')),
            ],
            options={
                'verbose_name': 'Topology',
                'verbose_name_plural': 'Topologies',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default=b'PY', max_length=2, choices=[(b'PY', b'Python'), (b'CP', b'C++')])),
                ('algorithm', models.CharField(default=b'GA', max_length=2, choices=[(b'GA', b'Genetic Algorithm'), (b'ES', b'Evolutives Strategy')])),
                ('git_repo', models.URLField(blank=True)),
                ('built_in', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, to='evolutives.Author', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessFunction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('c_type', models.CharField(default=b'RNG', max_length=3, choices=[(b'TXT', b'text'), (b'RNG', b'range'), (b'CHK', b'checkbox')])),
                ('c_min', models.IntegerField(default=1, null=True, blank=True)),
                ('c_max', models.IntegerField(default=100, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='code',
            name='parameters',
            field=models.ManyToManyField(to='evolutives.Parameter'),
        ),
    ]

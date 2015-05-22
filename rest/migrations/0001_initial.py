# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiTokens',
            fields=[
                ('username', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=150)),
                ('expiry', models.CharField(max_length=150)),
                ('active', models.IntegerField()),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20161221_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(default=20.58, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]

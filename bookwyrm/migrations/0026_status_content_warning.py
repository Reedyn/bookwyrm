# Generated by Django 3.0.7 on 2020-12-17 03:17

import bookwyrm.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookwyrm", "0025_auto_20201217_0046"),
    ]

    operations = [
        migrations.AddField(
            model_name="status",
            name="content_warning",
            field=bookwyrm.models.fields.CharField(
                blank=True, max_length=500, null=True
            ),
        ),
    ]

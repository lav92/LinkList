# Generated by Django 5.0.4 on 2024-04-20 18:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_alter_link_short_description_alter_link_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='owners',
        ),
        migrations.AddField(
            model_name='collection',
            name='owners',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collections', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_category_priority_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priority',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='priority',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-25 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_category_deleted_alter_category_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='deleted',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
    ]

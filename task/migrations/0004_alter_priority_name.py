# Generated by Django 5.1.2 on 2024-10-24 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_priority_deleted_alter_priority_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priority',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
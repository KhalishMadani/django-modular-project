# Generated by Django 4.2.20 on 2025-06-15 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('barcode', models.CharField(max_length=50, unique=True)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField(default=0)),
                ('dynamic_fields', models.JSONField(default=dict)),
            ],
        ),
    ]

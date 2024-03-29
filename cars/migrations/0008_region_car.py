# Generated by Django 4.2 on 2024-01-06 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_alter_modification_offers_price_from_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('price', models.PositiveBigIntegerField()),
                ('mileage', models.PositiveBigIntegerField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.brand')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.carmodel')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.region')),
            ],
            options={
                'db_table': 'car',
            },
        ),
    ]

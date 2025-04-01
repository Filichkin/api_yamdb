# Generated by Django 3.2 on 2025-04-01 17:37

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(unique=True, validators=[reviews.validators.validate_slug], verbose_name='Cлаг'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(unique=True, validators=[reviews.validators.validate_slug], verbose_name='Cлаг'),
        ),
    ]

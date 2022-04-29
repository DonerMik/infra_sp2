# Generated by Django 2.2.16 on 2022-01-23 11:25

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20220122_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(db_index=True, default=1, validators=[reviews.validators.year_validator]),
            preserve_default=False,
        ),
    ]

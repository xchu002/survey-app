# Generated by Django 4.0.6 on 2022-07-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveysite', '0005_survey_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='unique_id',
            field=models.CharField(max_length=6, null=True),
        ),
    ]

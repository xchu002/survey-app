# Generated by Django 4.0.6 on 2022-07-10 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveysite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='survey_question',
            new_name='test',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='user',
        ),
        migrations.DeleteModel(
            name='Response',
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-25 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0002_language_remove_cv_language_remove_cv_language_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagelevel',
            name='level',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='languagelevel',
            unique_together={('language', 'vacancy', 'level')},
        ),
    ]
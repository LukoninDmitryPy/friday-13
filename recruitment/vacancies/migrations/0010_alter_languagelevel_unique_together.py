# Generated by Django 4.2.6 on 2023-10-29 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0009_alter_languagelevel_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='languagelevel',
            unique_together=set(),
        ),
    ]

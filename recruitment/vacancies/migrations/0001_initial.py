# Generated by Django 4.2.6 on 2023-10-24 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import vacancies.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Город')),
                ('region', models.CharField(max_length=50, verbose_name='Регион')),
                ('country', models.CharField(max_length=50, verbose_name='Страна')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('IN', 'Intern'), ('JR', 'Junior'), ('MD', 'Middle'), ('SR', 'Senior'), ('LD', 'Lead')], max_length=2, verbose_name='Грейд')),
                ('is_remote_work', models.BooleanField(default=False, verbose_name='Удалёнка')),
                ('min_wage', models.PositiveIntegerField(verbose_name='Доход от')),
                ('max_wage', models.PositiveIntegerField(verbose_name='Доход до')),
                ('experience', models.CharField(choices=[('LOW', '0'), ('MED', '1-3'), ('HI', '3-6'), ('HIP', '6+')], max_length=5, verbose_name='Опыт работы')),
                ('currency', models.CharField(choices=[('RUB', '₽'), ('DOL', '$'), ('EURO', '€'), ('UAH', '₴')], max_length=5, verbose_name='Валюта')),
                ('language', models.CharField(choices=[('RU', 'Русский'), ('EU', 'English'), ('UA', 'Украинский')], max_length=2, verbose_name='Знание языка')),
                ('language_level', models.CharField(choices=[('A1', ''), ('A2', ''), ('B1', ''), ('B2', ''), ('C1', ''), ('C2', '')], max_length=2, verbose_name='Уровень языка')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Подробности')),
                ('requirements', models.TextField(verbose_name='Требования')),
                ('optional_requirements', models.TextField(verbose_name='Необязательные требования')),
                ('responsibility', models.TextField(verbose_name='Обязанности')),
                ('conditions', models.TextField(verbose_name='Условия')),
                ('selection_stages', models.TextField(verbose_name='Этапы отбора')),
                ('is_active', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('is_archive', models.BooleanField(default=False, verbose_name='Архивная')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=models.SET(vacancies.models.get_sentinel_user), to=settings.AUTH_USER_MODEL, verbose_name='Рекрутер')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vacancy', to='vacancies.city', verbose_name='Город')),
            ],
        ),
        migrations.CreateModel(
            name='Cv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('IN', 'Intern'), ('JR', 'Junior'), ('MD', 'Middle'), ('SR', 'Senior'), ('LD', 'Lead')], max_length=2, verbose_name='Грейд')),
                ('is_remote_work', models.BooleanField(default=False, verbose_name='Удалёнка')),
                ('min_wage', models.PositiveIntegerField(verbose_name='Доход от')),
                ('max_wage', models.PositiveIntegerField(verbose_name='Доход до')),
                ('experience', models.CharField(choices=[('LOW', '0'), ('MED', '1-3'), ('HI', '3-6'), ('HIP', '6+')], max_length=5, verbose_name='Опыт работы')),
                ('currency', models.CharField(choices=[('RUB', '₽'), ('DOL', '$'), ('EURO', '€'), ('UAH', '₴')], max_length=5, verbose_name='Валюта')),
                ('language', models.CharField(choices=[('RU', 'Русский'), ('EU', 'English'), ('UA', 'Украинский')], max_length=2, verbose_name='Знание языка')),
                ('language_level', models.CharField(choices=[('A1', ''), ('A2', ''), ('B1', ''), ('B2', ''), ('C1', ''), ('C2', '')], max_length=2, verbose_name='Уровень языка')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('optional_description', models.TextField(verbose_name='Немного о себе')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Рекрутер')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cv', to='vacancies.city', verbose_name='Город')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='vacancy',
            constraint=models.CheckConstraint(check=models.Q(('min_wage__lte', models.F('max_wage')), ('max_wage__exact', 0), _connector='OR'), name='check_min_wage_less_than_max_wage'),
        ),
    ]
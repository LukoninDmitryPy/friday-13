import recruitment.settings as ch

from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q, F
from django.contrib.auth import get_user_model

User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username="deleted")[0]


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Город')
    region = models.CharField(max_length=50, verbose_name='Регион')
    country = models.CharField(max_length=50, verbose_name='Страна')


class Expirience(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    company = models.CharField(max_length=150, verbose_name=("Компания"))
    title = models.CharField(max_length=150, verbose_name=("Должность"))
    description = models.CharField(max_length=150, verbose_name=("обязанности"))


class Language(models.Model):
    language = models.CharField(max_length=50, verbose_name='Язык')


class Params(models.Model):
    grade = models.CharField(max_length=2, choices=ch.GRADE, verbose_name=("Грейд"))
    work_format = models.CharField(max_length=5, choices=ch.WORK_FORMAT, verbose_name=("Формат работы"))
    currency = models.CharField(max_length=5, choices=ch.CURRENCY, verbose_name=("Валюта"))  # узнать CHOICES у дизайнеров и поменять

    class Meta:
        abstract = True


class Vacancy(Params):
    '''Модель вакансий.'''
    # уточнить обязательные поля у дизайнеров
    # проверка полей is_active is_archive
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), verbose_name=("Рекрутер"))  # лучше чтобы вакансия осталась у студентов при удалении рекрутера. Протестировать это
    title = models.CharField(max_length=200, null=False, verbose_name=("Название"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='vacancy', verbose_name='Город')
    description = models.TextField(verbose_name=("Подробности"))
    expirience = models.CharField(choices=ch.EXP, max_length=5, verbose_name=("Опыт работы"))
    responsibility = models.TextField(verbose_name=("Обязанности"))
    requirements = models.TextField(verbose_name=("Требования"))
    optional_requirements = models.TextField(verbose_name=("Необязательные требования"))
    conditions = models.TextField(verbose_name=("Условия"))
    selection_stages = models.TextField(verbose_name=("Этапы отбора"))
    min_wage = models.PositiveIntegerField(verbose_name=("Доход от"))
    max_wage = models.PositiveIntegerField(verbose_name=("Доход до"))
    is_active = models.BooleanField(default=True, verbose_name=("Опубликована"))
    is_archive = models.BooleanField(default=False, verbose_name=("Архивная"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(min_wage__lte=F('max_wage')) | Q(max_wage__exact=0),
                name='check_min_wage_less_than_max_wage',
            ),
        ]


class LanguageLevel(models.Model):
    LANG_LVL = [
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
    ]
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='language')
    level = models.CharField(max_length=2, choices=LANG_LVL)

    class Meta:
        unique_together = ('language', 'vacancy', 'level')


class Cv(Params):
    title = models.CharField(max_length=200, null=False, verbose_name=("Название"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='cv', verbose_name='Город')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Соискатель"))
    optional_description = models.TextField(verbose_name=("Немного о себе"))
    salary = models.IntegerField()
    expirience = models.ForeignKey(Expirience, on_delete=models.PROTECT)


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Applicant(Params):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.ForeignKey(City, on_delete=models.PROTECT, related_name='applicant', verbose_name='Город')
    is_winner = models.BooleanField()
    age = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    graduation_date = models.DateField()
    contacts = models.CharField(max_length=150)
    edu_status = models.PositiveSmallIntegerField(choices=ch.EDU_STATUS)
    work_status = models.PositiveSmallIntegerField(choices=ch.WORK_STATUS)
    salary = models.IntegerField()
    optional_description = models.TextField(verbose_name=("Немного о себе"))
    exp = models.ForeignKey(Expirience, on_delete=models.PROTECT, null=True)
    response_base_count = models.PositiveSmallIntegerField()
    test_task_count = models.PositiveSmallIntegerField()
    interview_count = models.PositiveSmallIntegerField()


class VacancyResponse(models.Model):
    STATUS = [
        (1, 'Отклик'),
        (2, 'Кандидат'),
        (3, 'Назначить интервью'),
        (4, 'Отправить тестовое'),
        (5, 'Тех. собеседование'),
        (6, 'Собеседование с руководителем'),
        (7, 'Тестовое задание'),
        (8, 'Отказ'),
        (9, 'Оффер'),
        (10, 'Отправить отказ'),
        (11, 'Отправить оффер'),
    ]
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='vacancy_responses', verbose_name='Соискатель')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancy_responses', verbose_name='Вакансия')
    status = models.PositiveSmallIntegerField(choices=STATUS, )

    class Meta:
        unique_together = ('applicant', 'vacancy')

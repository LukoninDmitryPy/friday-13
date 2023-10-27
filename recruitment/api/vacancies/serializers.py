from re import match
from rest_framework import serializers

from rest_framework.serializers import ValidationError

from vacancies.models import Cv, Vacancy, LanguageLevel, Expirience


class LanguageLevelSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=LanguageLevel.objects.all(),
        source='language.id',
    )
    language = serializers.ReadOnlyField(source='student.language')

    class Meta:
        model = LanguageLevel
        fields = ['id', 'language', 'level']


class CvCreateSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для создания резюме."""

    class Meta:
        model = Cv
        fields = (
            "title",
            "optional_description",
            "city",
            "salary",
            "experience",
            "currency",
        )

    def validate_name_cv(self, value):
        if match(r'^[-+]?[0-9]+$', value):
            raise ValidationError("Некорректное название резюме.")
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        cv = Cv.objects.create(author=author, **validated_data)
        return cv


class CvSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для работы с резюме."""

    class Meta:
        model = Cv
        fields = (
            "title",
            "optional_description",
            "city",
            "salary",
            "experience",
            "currency",
        )


class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор для вакансий."""
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    language = LanguageLevelSerializer(many=True)

    class Meta:
        model = Vacancy
        fields = (
            "author",
            "grade",
            "grade",
            "shedule",
            "currency"
            "title",
            "description",
            "requirements",
            "optional_requirements",
            "responsibility",
            "conditions",
            "selection_stages",
            "is_active",
            "is_archive",
            "created",

            "city",
            "min_wage",
            "max_wage",
            "currency",
            "language",
        )

    def validate_title_cv(self, value):
        if match(r'^[-+]?[0-9]+$', value):
            raise ValidationError("Некорректное название вакансии.")
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        vacancy = Vacancy.objects.create(author=author, **validated_data)
        return vacancy


# class VacancySerializer(serializers.ModelSerializer):
#     """Кастомный сериализатор для работы с вакансией."""

#     class Meta:
#         model = Vacancy
#         fields = (
#             "author",
#             "name",
#             "description",
#             "requirements",
#             "experience",
#             "optional_requirements",
#             "responsibility",
#             "conditions",
#             "selection_stages",
#             "is_active",
#             "is_archive",
#             "created",

#             "province",
#             "min_wage",
#             "max_wage",
#             "experience",
#             "currency",
#             "language",
#         )

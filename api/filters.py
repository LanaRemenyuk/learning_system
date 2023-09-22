from django_filters.rest_framework import FilterSet, filters
from .models import Lesson


class LessonFilter(FilterSet):
    product = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Lesson
        fields = ('product', )
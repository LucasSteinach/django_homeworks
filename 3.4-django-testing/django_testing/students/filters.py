from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from students.models import Course


class CourseFilter(filters.FilterSet):

    id = filters.ModelMultipleChoiceFilter(
        field_name="id",
        to_field_name="id",
        queryset=Course.objects.all(),
    )
    name = SearchFilter()

    class Meta:
        model = Course
        fields = ("id", "name", )

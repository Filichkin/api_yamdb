import django_filters

from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):
    """Фильтрация произведений по жанру, категории, названию, году."""

    category = django_filters.CharFilter(
        field_name='category__slug'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Titles
        fields = (
            'category',
            'genre',
            'name',
            'year'
        )

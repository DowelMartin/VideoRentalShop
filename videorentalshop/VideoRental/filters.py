import django_filters
from django.db.models import Q
from VideoRental.models import VideoTape


class VideoTapeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="in_text_search")

    class Meta:
        model = VideoTape
        fields = ["search"]

    def in_text_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value))

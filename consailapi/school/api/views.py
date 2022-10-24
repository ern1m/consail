from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from consailapi.school.api.serializers import MajorSerializer
from consailapi.school.models import Major


class MajorView(GenericViewSet, ListModelMixin):
    serializer_class = MajorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Major.objects.all()
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "id",
        "name",
    ]

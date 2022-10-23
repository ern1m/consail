from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from consailapi.school.api.serializers import MajorSerializer


class MajorView(GenericViewSet, ListModelMixin):
    serializer_class = MajorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "id",
        "name",
    ]

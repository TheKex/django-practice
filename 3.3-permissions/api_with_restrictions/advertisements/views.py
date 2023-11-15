from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly, IsAuthenticatedUpdate
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedUpdate]


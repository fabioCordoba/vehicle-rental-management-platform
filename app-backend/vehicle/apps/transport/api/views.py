from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.transport.models import Transport
from apps.transport.serializers import (
    TransportDetailSerializer,
    TransportSerializer,
    TransportWriteSerializer,
)


class TransportFilter(FilterSet):
    make = CharFilter(field_name="make", lookup_expr="icontains")
    model = CharFilter(field_name="model", lookup_expr="icontains")
    min_price = NumberFilter(field_name="daily_rental_price", lookup_expr="gte")
    max_price = NumberFilter(field_name="daily_rental_price", lookup_expr="lte")
    min_year = NumberFilter(field_name="year", lookup_expr="gte")
    max_year = NumberFilter(field_name="year", lookup_expr="lte")

    class Meta:
        model = Transport
        fields = ["make", "model", "is_available", "condition", "color"]


class TransportViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Transport.objects.filter(is_active=True).order_by("-created_at")
    filterset_class = TransportFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["make", "model", "license_plate", "color"]
    ordering_fields = ["year", "daily_rental_price", "mileage", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TransportWriteSerializer
        if self.action == "retrieve":
            return TransportDetailSerializer
        return TransportSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "available", "search_by_status", "search"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.disable()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="available")
    def available(self, request):
        """Returns only vehicles currently available for rental."""
        queryset = self.filter_queryset(
            self.get_queryset().filter(is_available=True)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TransportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="search-by-status")
    def search_by_status(self, request):
        """Filter vehicles by availability status. Query param: ?status=available|unavailable"""
        status_param = request.query_params.get("status", "").lower()
        if status_param == "available":
            is_available = True
        elif status_param == "unavailable":
            is_available = False
        else:
            return Response(
                {"detail": "Invalid status. Use 'available' or 'unavailable'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.filter_queryset(
            self.get_queryset().filter(is_available=is_available)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TransportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Búsqueda de vehículos por marca, modelo y/o estado de disponibilidad.

        Query params:
          ?make=<texto>              — marca (búsqueda parcial, insensible a mayúsculas)
          ?model=<texto>             — modelo (búsqueda parcial, insensible a mayúsculas)
          ?status=available          — solo disponibles
          ?status=unavailable        — solo no disponibles

        Se pueden combinar libremente. Sin parámetros retorna todos los vehículos activos.
        """
        queryset = self.get_queryset()

        make = request.query_params.get("make", "").strip()
        model = request.query_params.get("model", "").strip()
        status_param = request.query_params.get("status", "").strip().lower()

        if make:
            queryset = queryset.filter(make__icontains=make)

        if model:
            queryset = queryset.filter(model__icontains=model)

        if status_param == "available":
            queryset = queryset.filter(is_available=True)
        elif status_param == "unavailable":
            queryset = queryset.filter(is_available=False)
        elif status_param:
            return Response(
                {"detail": "Valor de 'status' inválido. Use 'available' o 'unavailable'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TransportSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TransportSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["patch"],
        url_path="toggle-availability",
        permission_classes=[IsAdminUser],
    )
    def toggle_availability(self, request, pk=None):
        """Toggle the is_available flag of a transport vehicle."""
        transport = self.get_object()
        transport.is_available = not transport.is_available
        transport.save(update_fields=["is_available", "updated_at"])
        serializer = TransportDetailSerializer(transport)
        return Response(serializer.data)

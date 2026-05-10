from rest_framework import mixins, viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.procedure.models import Procedure
from apps.procedure.api.serializers import ProcedureSerializer, ProcedureWriteSerializer


class ProcedureViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "vehicle_id", "customer_id"]
    search_fields = ["status"]
    ordering_fields = ["request_date", "start_date", "end_date", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Procedure.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProcedureWriteSerializer
        return ProcedureSerializer

    def destroy(self, request, *args, **kwargs):
        procedure = self.get_object()
        procedure.is_active = False
        procedure.save(update_fields=["is_active"])
        return Response(
            {"detail": "Procedure deactivated successfully."},
            status=status.HTTP_200_OK,
        )

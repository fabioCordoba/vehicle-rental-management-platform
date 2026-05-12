from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.procedure.models import Procedure
from apps.procedure.api.serializers import ProcedureSerializer, ProcedureWriteSerializer
from apps.procedure.services.vehicle_client import toggle_vehicle_availability


def _extract_token(request) -> str:
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return auth_header


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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["token"] = _extract_token(self.request)
        return context

    def destroy(self, request, *args, **kwargs):
        procedure = self.get_object()
        procedure.is_active = False
        procedure.save(update_fields=["is_active"])
        return Response(
            {"detail": "Procedure deactivated successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"], url_path="confirm")
    def confirm(self, request, pk=None):
        """
        Confirm a pending rental request.
        Marks the procedure as ACTIVE and sets the vehicle as unavailable
        via the vehicle microservice.
        """
        procedure = self.get_object()

        if procedure.status != Procedure.Status.PENDING:
            return Response(
                {"detail": "Only pending procedures can be confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = _extract_token(request)
        vehicle_data = toggle_vehicle_availability(str(procedure.vehicle_id), token)
        if vehicle_data is None:
            return Response(
                {"detail": "Failed to update vehicle availability. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Guard: if the vehicle was already unavailable the toggle made it available,
        # so we need to toggle back and reject the confirmation.
        if vehicle_data.get("is_available"):
            toggle_vehicle_availability(str(procedure.vehicle_id), token)
            return Response(
                {"detail": "Vehicle is not available for rental."},
                status=status.HTTP_409_CONFLICT,
            )

        procedure.status = Procedure.Status.ACTIVE
        procedure.save(update_fields=["status", "updated_at"])
        return Response(ProcedureSerializer(procedure).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="cancel")
    def cancel(self, request, pk=None):
        """
        Cancel a pending or active rental request.
        If the procedure was ACTIVE, restores vehicle availability
        via the vehicle microservice.
        """
        procedure = self.get_object()

        if procedure.status in (Procedure.Status.COMPLETED, Procedure.Status.CANCELLED):
            return Response(
                {"detail": "Cannot cancel a completed or already cancelled procedure."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if procedure.status == Procedure.Status.ACTIVE:
            token = _extract_token(request)
            vehicle_data = toggle_vehicle_availability(str(procedure.vehicle_id), token)
            if vehicle_data is None:
                return Response(
                    {"detail": "Failed to restore vehicle availability. Please try again."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        procedure.status = Procedure.Status.CANCELLED
        procedure.save(update_fields=["status", "updated_at"])
        return Response(ProcedureSerializer(procedure).data, status=status.HTTP_200_OK)

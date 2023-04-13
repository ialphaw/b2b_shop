from django.db import transaction

from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Charge, UserCredit
from shop.serializers import ChargeSerializer


class ChargeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChargeSerializer
    http_method_names = ("get", "post")

    def get_queryset(self):
        queryset = Charge.objects.all().order_by("-id")
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a charge"""

        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission for this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)

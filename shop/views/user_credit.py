from django.core.exceptions import ValidationError

from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import UserCredit
from shop.serializers import UserCreditSerializer
from shop.helpers import make_transaction


class UserCreditViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserCreditSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        queryset = UserCredit.objects.all().order_by("-id")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'POST' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(
        detail=False, methods=["POST"], permission_classes=[permissions.IsAdminUser]
    )
    def increase_credit(self, request):
        """Increase credit for a user"""

        try:
            data = request.data
            username = data["username"]
            credit = data["credit"]
        except KeyError as e:
            print(str(e))
            raise exceptions.ValidationError(
                detail="Bad Json", code=status.HTTP_400_BAD_REQUEST
            )

        instance, created = UserCredit.objects.get_or_create(user__username=username)

        make_transaction("i", credit, instance.user)

        return Response({"message": "Credit increased successfully"})

    @action(detail=True, methods=["POST"])
    def purchase(self, request, pk=None):
        """Purchase a charge"""

        user = request.user

        try:
            charge_amount = int(request.data["charge_amount"])
        except KeyError as e:
            print(str(e))
            raise exceptions.ValidationError(
                detial="Bad Json", code=status.HTTP_400_BAD_REQUEST
            )

        try:
            make_transaction("d", charge_amount, user)
        except ValidationError:
            raise exceptions.ValidationError(
                detail="You do not have the required credit",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Your purchase has been done successfully"})

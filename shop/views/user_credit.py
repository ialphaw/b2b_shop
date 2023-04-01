from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import UserCredit
from shop.serializers import UserCreditSerializer


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
            return exceptions.ValidationError(
                detail="Bad Json", code=status.HTTP_400_BAD_REQUEST
            )

        instance, created = UserCredit.objects.get_or_create(user__username=username)
        instance.credit = instance.credit + credit
        instance.save(update_fields=["credit"])

        return Response({"message": "Credit increased successfully"})

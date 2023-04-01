from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import Charge, UserCredit
from shop.serializers import ChargeSerializer


class ChargeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpass", is_staff=True
        )
        self.charge = Charge.objects.create(name="Test Charge", amount=10)

    def test_list_charges(self):
        self.client.force_login(self.user)
        url = "/api/v1/shop/charge/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_charge(self):
        self.client.force_login(self.user)
        url = f"/api/v1/shop/charge/{self.charge.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_charge(self):
        self.client.force_login(self.staff_user)
        url = "/api/v1/shop/charge/"
        data = {"name": "New Charge", "amount": 15}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_purchase_charge(self):
        self.client.force_login(self.user)
        user_credit = UserCredit.objects.create(user=self.user, credit=20)
        url = f"/api/v1/shop/charge/{self.charge.pk}/purchase/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_credit.refresh_from_db()
        self.assertEqual(
            user_credit.credit, 10
        )  # credit should be reduced by 10 after purchase

    def test_purchase_charge_insufficient_credit(self):
        self.client.force_login(self.user)
        user_credit = UserCredit.objects.create(user=self.user, credit=5)
        url = f"/api/v1/shop/charge/{self.charge.pk}/purchase/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_credit.refresh_from_db()
        self.assertEqual(
            user_credit.credit, 5
        )  # credit should not be reduced after failed purchase

    def test_purchase_charge_no_credit(self):
        self.client.force_login(self.user)
        url = f"/api/v1/shop/charge/{self.charge.pk}/purchase/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

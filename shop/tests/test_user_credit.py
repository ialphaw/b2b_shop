from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import UserCredit


class UserCreditViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.user_credit1 = UserCredit.objects.create(user=self.user1, credit=100.0)
        self.user_credit2 = UserCredit.objects.create(user=self.user2, credit=200.0)

    def test_list_user_credit(self):
        # Authenticate as a regular user
        self.client.force_authenticate(user=self.user1)

        # Make GET request to the list endpoint
        response = self.client.get("/api/v1/shop/user_credit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that only the user's own credits are returned
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["user"]["username"], "user1")
        self.assertEqual(response.data["results"][0]["credit"], "100.00")

    def test_increase_credit_as_admin(self):
        # Authenticate as an admin
        self.client.force_authenticate(user=self.admin)

        # Make POST request to the increase_credit endpoint
        data = {"username": "user1", "credit": 50}
        response = self.client.post("/api/v1/shop/user_credit/increase_credit/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the credit has been increased
        user_credit = UserCredit.objects.get(user=self.user1)
        self.assertEqual(user_credit.credit, 150.0)

    def test_increase_credit_as_regular_user(self):
        # Authenticate as a regular user
        self.client.force_authenticate(user=self.user1)

        # Make POST request to the increase_credit endpoint
        data = {"username": "user2", "credit": 50.0}
        response = self.client.post("/api/v1/shop/user_credit/increase_credit/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify that the credit has not been increased
        user_credit = UserCredit.objects.get(user=self.user2)
        self.assertEqual(user_credit.credit, 200.0)

import time
import json
from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import UserCredit


class PurchaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.client.force_login(self.user)
        self.user_credit = UserCredit.objects.create(user=self.user, credit=2000)

    def test_purchase_response_time_one_request_per_second(self):
        self.client.force_login(self.user)
        data = json.dumps({"charge_amount": 10})
        start_time = time.monotonic()
        response = self.client.post(
            f"/api/v1/shop/user_credit/{self.user_credit.id}/purchase/",
            data,
            content_type="application/json",
        )
        end_time = time.monotonic()
        response_time = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(response_time, 1.0)

    def test_purchase_response_time_twenty_requests_per_second(self):
        self.client.force_login(self.user)
        data = json.dumps({"charge_amount": 10})
        start_time = time.monotonic()
        for i in range(20):
            response = self.client.post(
                f"/api/v1/shop/user_credit/{self.user_credit.id}/purchase/",
                data,
                content_type="application/json",
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            time.sleep(0.05)
        end_time = time.monotonic()
        response_time = (end_time - start_time) / 20
        self.assertLess(response_time, 1.0)

    def test_purchase_response_time_twenty_parallel_requests(self):
        response_times = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(20):
                future = executor.submit(self.send_request)
                futures.append(future)
                time.sleep(0.05)
            for future in futures:
                response_times.append(future.result())
        total_response_time = sum(response_times)
        average_response_time = total_response_time / len(response_times)
        self.assertLessEqual(average_response_time, 0.5, "Response time is too high")

    def send_request(self):
        data = json.dumps({"charge_amount": 10})
        start_time = time.monotonic()
        response = self.client.post(
            f"/api/v1/shop/user_credit/{self.user_credit.id}/purchase/",
            data,
            content_type="application/json",
        )
        end_time = time.monotonic()
        response_time = end_time - start_time
        return response_time

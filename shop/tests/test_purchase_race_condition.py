import json
from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from shop.models import UserCredit, Transaction, Charge


class ChargeViewSetTestCase(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.staff_user = User.objects.create_user(
            username="staffuser", password="staffpass", is_staff=True
        )
        # self.charge = Charge.objects.create(name="Test Charge", amount=10)
        self.user_credit = UserCredit.objects.create(user=self.user, credit=1000.0)

    def test_purchase_race_condition(self):
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for i in range(100):
                future = executor.submit(self.send_purchase_request)
                futures.append(future)

            for future in futures:
                future.result()

        self.assertEqual(
            Transaction.objects.filter(user=self.user, category="d").count(), 100
        )

    def send_purchase_request(self):
        self.client.force_login(self.user)
        data = json.dumps({"charge_amount": 10})
        response = self.client.post(
            f"/api/v1/shop/user_credit/{self.user_credit.id}/purchase/",
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": "Your purchase has been done successfully"}
        )

from rest_framework.exceptions import APIException


class BalanceInsufficient(APIException):
    status_code = 400
    default_detail = "You do not have the required credit"
    default_code = "balance_insufficient"

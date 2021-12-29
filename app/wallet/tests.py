from django.test import TestCase

from users.models import User
from wallet.models import Wallet, Transfer


class TestWallet(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user("mock_user@user.com", "mockusername", "mock", "user", "123456")
        self.user_2 = User.objects.create_user("mock_user2@user.com", "mockusername2", "mock2", "user2", "123456")
        self.wallet_1 = Wallet(owner=self.user_1, balance=1000)
        self.wallet_1.save()
        self.assertIsNotNone(self.wallet_1)
        self.wallet_2 = Wallet(owner=self.user_2, balance=1000)
        self.wallet_2.save()

    def test_transfer(self):
        transfer = Transfer(source=self.wallet_1, destination=self.wallet_2, amount=200)
        transfer.save()
        self.assertEqual(self.wallet_1.balance, 800)
        self.assertEqual(self.wallet_2.balance, 1200)

    def test_insufficient_balance_transfer(self):
        transfer = Transfer(source=self.wallet_1, destination=self.wallet_2, amount=2000)
        self.assertRaises(ValueError, transfer.transfer_money)

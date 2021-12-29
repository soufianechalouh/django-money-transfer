from rest_framework import serializers

from wallet.models import Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"

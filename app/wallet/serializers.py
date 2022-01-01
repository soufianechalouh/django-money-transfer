from rest_framework import serializers

from wallet.models import Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Wallet
        fields = ("owner", "balance", "status")
        read_only_fields = ("balance", "status")


class TransferSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="source.username", read_only=True)
    receiver = serializers.CharField(source="destination.username")

    class Meta:
        model = Transfer
        fields = ["sender", "receiver", "created_at", "amount", "status"]
        read_only_fields = ("sender", "created_at", "status")

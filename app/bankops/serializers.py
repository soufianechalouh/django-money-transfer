from rest_framework import serializers

from bankops.models import Withdraw, Topup


class WithdrawSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Withdraw
        fields = ("user", "status", "amount", "transaction_id")
        read_only_fields = ("status", "transaction_id")


class TopupSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Topup
        fields = "__all__"
        read_only_fields = ("status", "user", "transaction_id")


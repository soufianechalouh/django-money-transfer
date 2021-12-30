from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from wallet.models import Wallet, Transfer
from wallet.serializers import WalletSerializer, TransferSerializer


class WalletViewset(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Wallet.objects.all()
        return Wallet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransferViewset(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = TransferSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transfer.objects.all()
        return Transfer.objects.filter(Q(source__owner=self.request.user) | Q(destination__owner=self.request.user))

    def perform_create(self, serializer):
        if not User.objects.count(username=serializer.validated_data["destination"]["username"]):
            raise ValueError("Destination user does not exist")
        destination = User.objects.get(username=serializer.validated_data["destination"]["username"])
        serializer.save(source=self.request.user, destination=destination)

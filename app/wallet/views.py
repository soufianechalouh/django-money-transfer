from rest_framework import viewsets

from wallet.models import Wallet, Transfer
from wallet.serializers import WalletSerializer, TransferSerializer


# TODO (soufiane): set permissions and restrict access
class WalletViewset(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()


class TransferViewset(viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()

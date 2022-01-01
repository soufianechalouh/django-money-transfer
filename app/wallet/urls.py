from django.urls import path

from wallet.views import WalletViewset, TransferViewset

urlpatterns = [
    path("wallets/", WalletViewset.as_view()),
    path("transfers/", TransferViewset.as_view())
]

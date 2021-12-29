from rest_framework import routers
from django.urls import path, include

from wallet.views import WalletViewset, TransferViewset

router = routers.DefaultRouter()
router.register("wallets", WalletViewset)
router.register("transfers", TransferViewset)

urlpatterns = [
    path("", include(router.urls))
]

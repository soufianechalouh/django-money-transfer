from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Withdraw, Topup
from .serializers import WithdrawSerializer, TopupSerializer


class WithdrawViewset(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Withdraw.objects.all()
        return Withdraw.objects.filter(user=self.request.user)


class TopupViewset(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TopupSerializer

    def get_queryset(self):
        return Topup.objects.filter(user=self.request.user)

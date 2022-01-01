from django.urls import path

from bankops.views import WithdrawViewset, TopupViewset

urlpatterns = [
    path("withdraws/", WithdrawViewset.as_view()),
    path("topups/", TopupViewset.as_view())
]

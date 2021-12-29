from django.urls import path, include
from rest_framework import routers

from submissions.views import SubmissionViewset

router = routers.DefaultRouter()
router.register("submissions", SubmissionViewset)

urlpatterns = [
    path("", include(router.urls))
]

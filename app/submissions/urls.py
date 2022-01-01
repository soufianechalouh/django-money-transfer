from django.urls import path, include
from rest_framework import routers

from submissions.views import SubmissionViewset, SubmissionListViewset

router = routers.DefaultRouter()
router.register("submissions", SubmissionViewset)

urlpatterns = [
    path("submissions-list/", SubmissionListViewset.as_view()),
    path("", include(router.urls))
]

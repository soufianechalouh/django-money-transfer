from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Submission
from .serializers import SubmissionListCreateSerializer, SubmissionSerializer


class SubmissionViewset(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()


class SubmissionListViewset(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionListCreateSerializer
    lookup_field = "id"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Submission.objects.all()
        return Submission.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

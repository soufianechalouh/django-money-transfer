from django.db import models

from users.models import User


class Submission(models.Model):
    SUBMISSION_STATUS_CHOICES = [(x, x) for x in ["DRAFT", "SUBMITTED", "IN_REVIEW", "VALIDATED", "DECLINED"]]
    ID_TYPE_CHOICES = [(x, x) for x in ["ID_CARD", "DRIVER_LICENSE", "PASSPORT"]]

    user = models.ForeignKey(User, related_name="submission", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, limit_choices_to={'is_staff': True}, null=True,
                                 related_name="submissions", on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=SUBMISSION_STATUS_CHOICES)
    id_document = models.ImageField()
    selfie = models.ImageField()
    document_type = models.CharField(max_length=32, choices=ID_TYPE_CHOICES)
    review = models.CharField(max_length=512, null=True, blank=True)

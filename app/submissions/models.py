from django.db import models

from users.models import User

from django.db.models.signals import post_save


class Submission(models.Model):
    DRAFT = 'DR'
    SUBMITTED = 'SU'
    IN_REVIEW = 'IR'
    VERIFIED = 'VF'
    ESCALATED = 'ES'
    DECLINED = 'DC'
    SUBMISSION_STATUS_CHOICES = [
        (DRAFT, 'DRAFT'),
        (SUBMITTED, 'SUBMITTED'),
        (IN_REVIEW, 'IN_REVIEW'),
        (VERIFIED, 'VERIFIED'),
        (ESCALATED, 'ESCALATED'),
        (DECLINED, 'DECLINED'),
    ]
    ID_TYPE_CHOICES = [(x, x) for x in ["ID_CARD", "DRIVER_LICENSE", "PASSPORT"]]

    user = models.ForeignKey(User, related_name="submission", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, limit_choices_to={'is_staff': True}, null=True,
                                 related_name="submissions", on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=SUBMISSION_STATUS_CHOICES, default=SUBMITTED)
    id_code = models.CharField(max_length=10, null=True)
    id_document = models.ImageField()
    selfie = models.ImageField()
    document_type = models.CharField(max_length=32, choices=ID_TYPE_CHOICES)
    review = models.CharField(max_length=512, null=True, blank=True)


def submission_post_save(sender, instance, created,  *args, **kwargs):
    if instance.status == Submission.VERIFIED and instance.user.is_verified is False:
        user = instance.user
        user.is_verified = True
        user.save()


post_save.connect(submission_post_save, sender=Submission)

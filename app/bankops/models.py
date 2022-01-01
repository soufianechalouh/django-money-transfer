from random import randint

from django.db import models

from users.models import User
from wallet.models import AbstractTransaction


class Withdraw(AbstractTransaction):
    """
        Withdraw operations model
        :param : Processed status refers to when the operation is completed and the money is withdrawn
    """
    AWAITING_VALIDATION = 'WV'
    VALIDATED = 'VA'
    PROCESSED = 'PR'
    CANCELED = 'CA'
    WITHDRAW_STATUS_CHOICES = [
        (AWAITING_VALIDATION, 'WAIT_FOR_VALIDATION'),
        (VALIDATED, 'VALIDATED'),
        (PROCESSED, 'PROCESSED'),
        (CANCELED, 'CANCELED')
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=6, choices=WITHDRAW_STATUS_CHOICES, default=AWAITING_VALIDATION)
    validation_code = models.CharField(max_length=6, blank=True)
    transaction_id = models.CharField(max_length=32, null=True)

    def save(self, *args, **kwargs):
        if not self.validation_code:
            self.validation_code = str(randint(100000, 999999))
            # send validation code to user

        super(Withdraw, self).save(*args, **kwargs)

    def confirm_withdraw(self, code):
        if self.validation_code == code:
            self.status = self.VALIDATED
        else:
            self.status = self.CANCELED
        self.save()


class Topup(AbstractTransaction):
    PROCESSING = 'PG'
    PROCESSED = 'PR'
    FAILED = 'FAILED'
    TOPUP_STATUS_CHOICES = [
        (PROCESSING, 'PROCESSING'),
        (PROCESSED, 'PROCESSED'),
        (FAILED, 'FAILED')
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=6, choices=TOPUP_STATUS_CHOICES, default=PROCESSING)
    transaction_id = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        # execute redirection to payment processor, do the function that does the bank magic to complete the operation
        # if it works, credit the wallet and mark operation as processed
        # if it doesn't, mark the operation as failed
        super(Topup, self).save(*args, **kwargs)

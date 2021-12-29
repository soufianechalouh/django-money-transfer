from django.core.validators import MinValueValidator
from django.db import models, transaction

from users.models import User


class Wallet(models.Model):
    ACTIVE = 'AC'
    ON_HOLD = 'ON'
    ARCHIVED = 'AR'
    WALLET_STATUS_CHOICES = [
        (ACTIVE, 'ACTIVE'),
        (ON_HOLD, 'ON_HOLD'),
        (ARCHIVED, 'ARCHIVED')
    ]
    owner = models.ForeignKey(User, related_name="wallet", on_delete=models.CASCADE)
    balance = models.FloatField(default=0, blank=True, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=2, choices=WALLET_STATUS_CHOICES, default=ACTIVE, blank=True)


class AbstractTransaction(models.Model):
    """Common properties between transactions (Transfer, withdraw, and refill)"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class Transfer(AbstractTransaction):
    """Operations from one wallet on another"""
    IN_PROGRESS = "IP"
    EXECUTED = "EX"
    CANCELED = "CA"
    TRANSFER_STATUS_CHOICES = [
        (IN_PROGRESS, 'IN_PROGRESS'),
        (EXECUTED, 'EXECUTED'),
        (CANCELED, 'CANCELED')
    ]
    source = models.OneToOneField(Wallet, related_name="transfers", on_delete=models.SET)
    destination = models.OneToOneField(Wallet, on_delete=models.SET)
    status = models.CharField(max_length=2, choices=TRANSFER_STATUS_CHOICES, default=IN_PROGRESS, blank=True)
    log = models.TextField(null=True, blank=True)

    @transaction.atomic
    def transfer_money(self):
        source = self.source
        destination = self.destination
        if source.balance < self.amount:
            raise ValueError("Insufficient balance")
        if source.status != Wallet.ACTIVE:
            raise ValueError("Source wallet inactive")
        if destination.status != Wallet.ACTIVE:
            raise ValueError("Destination wallet inactive")
        source.balance -= self.amount
        destination.balance += self.amount
        source.save()
        destination.save()

    def execute_transaction(self):
        try:
            self.transfer_money()
        except Exception as e:
            self.log = str(e)
            self.status = self.CANCELED
            self.save()

    def save(self, *args, **kwargs):
        super(Transfer, self).save(*args, *kwargs)

        if self.status == self.IN_PROGRESS:
            self.execute_transaction()

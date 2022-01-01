from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models.signals import post_save

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
    owner = models.OneToOneField(User, related_name="wallet", on_delete=models.CASCADE)
    balance = models.FloatField(default=0, blank=True, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=2, choices=WALLET_STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return f"{self.owner.username}'s wallet"


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
    source = models.ForeignKey(User, related_name="transfers", to_field='username',
                               null=True, on_delete=models.SET_NULL)
    destination = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=TRANSFER_STATUS_CHOICES, default=IN_PROGRESS)
    log = models.TextField(null=True, blank=True)

    @transaction.atomic
    def transfer_money(self):
        source_wallet = self.source.wallet
        destination_wallet = self.destination.wallet
        if source_wallet.balance < self.amount:
            raise ValueError("Insufficient balance")
        if source_wallet.status != Wallet.ACTIVE:
            raise ValueError("Source wallet inactive")
        if destination_wallet.status != Wallet.ACTIVE:
            raise ValueError("Destination wallet inactive")
        source_wallet.balance -= self.amount
        destination_wallet.balance += self.amount
        source_wallet.save()
        destination_wallet.save()

    def execute_transaction(self):
        try:
            self.transfer_money()
            self.status = self.EXECUTED
            self.save()
        except Exception as e:
            self.log = str(e)
            self.status = self.CANCELED
            self.save()


def transfer_post_save(sender, instance, created,  *args, **kwargs):
    if instance.status == Transfer.IN_PROGRESS:
        instance.execute_transaction()


post_save.connect(transfer_post_save, sender=Transfer)

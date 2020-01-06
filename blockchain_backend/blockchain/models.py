from django.db import models


class Account(models.Model):
    pubkey = models.CharField(
        max_length=255,
    )

    balance_timestamp = models.DateTimeField(
        blank=True, null=True,
    )

    balance_nanoabend = models.BigIntegerField(
        blank=True, null=True,
    )

    balance_nanoaeter = models.BigIntegerField(
        blank=True, null=True,
    )

    label = models.CharField(
        max_length=255,
        default="",
    )

    def __str__(self):
        return "%s (%f AB, %f AE)" % (self.pubkey, self.balance_nanoabend / 1e9, self.balance_nanoaeter / 1e9)


class APILog(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    method = models.CharField(
        max_length=255,
    )

    args = models.TextField()

    result = models.TextField()

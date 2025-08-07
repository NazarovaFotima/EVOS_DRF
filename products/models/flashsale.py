from django.db import models
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from .product import Product


class FlashSale(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_percentage= models.PositiveIntegerField()
    start_time= models.DateTimeField()
    end_time= models.DateTimeField()


    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time


    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

    @property
    def status(self):
        if self.is_active():
            return "active"
        elif timezone.now() < self.start_time:
            return "upcoming"
        else:
            return "expired"

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
        ]

        unique_together = ('product', 'start_time', 'end_time')


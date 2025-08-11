from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .product import Product

User = get_user_model()

class Customer(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name= models.CharField(null=False, blank=False, max_length=100)
    phone_number= models.CharField(
        unique=True,
        max_length=15,
        verbose_name="Phone Number",
        help_text="Enter a valid phone number (e.g., +998XXXXXXXXX)"
    )

    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating between 1 and 5"
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} - {self.rating}"


class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', '-timestamp']),  # Recent views by user
            models.Index(fields=['product', '-timestamp']),  # Popularity
        ]
        # Optional: Prevent duplicates
        unique_together = ('user', 'product', 'timestamp')  # Or just (user, product) if dedup needed
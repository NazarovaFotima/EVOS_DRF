from django.db import models


class Category(models.Model):
    title=models.CharField(null=False, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,)
    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=False, blank=False)
    category= models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    cost = models.IntegerField(null=False, blank=False, )
    price= models.IntegerField(null=False, blank=False)
    # image= models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)  # New field for stock

    def __str__(self):
        return self.title

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            return False

        self.stock -= quantity
        self.save()
        return True

    def increase_stock(self, amount):
        self.stock += amount
        self.save()

    class Meta:
        ordering = ['title']
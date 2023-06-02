from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=12345)
    image = models.ImageField(upload_to='app/images', max_length=100)


class Product(models.Model):
    slug = models.SlugField(max_length=48, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField( )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='app/images', max_length=100)
    quantity = models.PositiveIntegerField()

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    prodquan = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}-{self.user}-{self.purchase_time}"


class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='purchase')
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purchase}-{self.request_time}"


from django.db import models
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)

    @property
    def get_absolute_url(self):
        return self.image.url

    @property
    def discounted_price(self):
        if self.discount > 0:
            self.price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return Decimal(self.price).quantize(Decimal('0.001'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Order(BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(region="UZ")
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name} => {self.phone_number}'


class Comment(BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='comments',
                                null=True, blank=True)
    is_negative = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.full_name} => {self.created_at}'

    class Meta:
        # verbose_name = 'comment'
        ordering = ['-created_at']

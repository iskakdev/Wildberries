from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MinValueValidator(15),
                                                  MaxValueValidator(77)], null=True, blank=True)
    STATUS_CHOICE = (
        ('GOLD', 'GOLD'),
        ('SILVER', 'SILVER'),
        ('BRONZE', 'BRONZE'),
        ('SIMPLE', 'SIMPLE')
    )
    phone_number = PhoneNumberField()
    status = models.CharField(max_length=55, choices=STATUS_CHOICE, default='SIMPLE')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_image = models.ImageField(null=True, blank=True)
    category_name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
    subcategory_name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f'{self.subcategory_name}'


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=55)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    article_number = models.PositiveIntegerField(unique=True)
    description = models.TextField()
    product_type = models.BooleanField()
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_name}'

    def avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.stars for i in ratings]) / ratings.count(), 1)
        return 0

    def count_people(self):
        ratings = self.reviews.all()
        return ratings.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(null=True, blank=True)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    add_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}, {self.quantity}'

    def get_total_price(self):
        return self.quantity * self.product.price
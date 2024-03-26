from django.db import models
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User

STATUS_CHOICE = (
    ("proccessing", "Precessing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In review"),
    ("published", "Published"),
)


RATING = ((1, "★☆☆☆☆"), (2, "★★☆☆☆"), (3, "★★★☆☆"), (4, "★★★★☆"), (5, "★★★★★"))


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


def get_image_upload_path(instance, filename):
    return f"product-images/{instance.product.title}/{filename}"


# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(
        unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True, length=10, max_length=30, editable=False,prefix="vend", alphabet="abcdefgh"
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, default="1 Main Street.")
    contact = models.CharField(max_length=100, default="+380 069 412 4100")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="1")
    authentic_rating = models.CharField(max_length=100, default="1")
    days_return = models.CharField(max_length=100, default="1")
    warranty_period = models.CharField(max_length=100, default="1")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendor"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Product(models.Model):
    pid = ShortUUIDField(
        unique=True, length=10, max_length=20, prefix="prd", alphabet="abcdefgh"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="category"
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")

    description = models.TextField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=9999, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=9999, decimal_places=2, null=True, blank=True
    )

    weight = models.CharField(max_length=10, default="1kg")
    specifications = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review"
    )
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(
        unique=True, length=5, max_length=10, prefix="sku", alphabet="1234567890"
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        if self.old_price and self.price < self.old_price:
            new_price = (self.price - self.old_price) / self.old_price
            new_price_in_percent = new_price * 100 if new_price != 1 else 0
            return new_price_in_percent
        return 0


class ProductImages(models.Model):
    images = models.ImageField(upload_to=get_image_upload_path, default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"


################################################################### Cart, Order, OrderItems   ###################################################################
################################################################### Cart, Order, OrderItems   ###################################################################
################################################################### Cart, Order, OrderItems   ###################################################################
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=9999, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=30, default="processing"
    )

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999, decimal_places=2)
    total = models.DecimalField(max_digits=9999, decimal_places=2)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50">' % (self.image))


################################################################### PRODUCT review, WishList, Address ###################################################################
################################################################### PRODUCT review, WishList, Address ###################################################################
################################################################### PRODUCT review, WishList, Address ###################################################################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products reviews"

    def __str__(self):
        return self.product.title

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price

    def get_rating(self):
        return self.rating


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title

    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price

    def get_rating(self):
        return self.rating


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

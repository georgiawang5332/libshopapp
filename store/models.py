from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils import timezone

class ProductManage(models.Manager):
    def all (self, *args, **kwargs):
        # Product.objects.all() = super(PostManage, self).all()
        return super(ProductManage, self).filter(draft=False).filter(timestamp__lte=timezone.now())

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

def imgs(instance, filename):
    return "%s/%s" % (instance.id, filename)

class RegistrationData(models.Model):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return str(self.email)

class Product(models.Model):
    name     = models.CharField(max_length=200)
    content  = models.TextField(default='')
    price    = models.DecimalField(max_digits=7, decimal_places=2)
    digital  = models.BooleanField(default=False, null=True, blank=True)
    draft    = models.BooleanField(default=False)
    image    = models.ImageField(
        upload_to=imgs,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
    )
    height_field = models.IntegerField(default=0)
    width_field  = models.IntegerField(default=0)
    updated      = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp    = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = ProductManage()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={'id': self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils import timezone
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
    # 現在刪除 與 發布刪除 信號
    pre_delete,
    post_delete,
    m2m_changed,
)
from django.utils import timezone


class ProductManage(models.Manager):
    def active(self, *args, **kwargs):
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


# User = settings.AUTH_USER_MODEL
class Product(models.Model):
    user = models.ForeignKey(User, default=1, db_constraint=False,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField(default='')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    draft = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=imgs,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)
    notify_user = models.BooleanField(default=False)
    notify_user_timestamp = models.DateTimeField(blank=True, null=True, auto_now_add=False)
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

# 20210330 Defining and sending signals 添加 pre_save & post_save or pre_del & post_del 等 https://docs.djangoproject.com/en/3.1/ref/signals信號/
@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    # if instance.id and instance.notify_user:
    #     print("notify users - 通知用戶!!!")
    #     instance.notify_user = False
    #     # celery worker task -> offload -> Time & task 2 cfe.sh 芹菜工人任務->卸載
    #     instance.notify_user_timestamp = timezone.now()

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, *args, **kwargs):
    # # instance = Product.objects.create() #save Product data in the db
    # if not instance.slug:
    #     instance.slug = slugify(instance.name)  # this is my name -> this-is-my-name
    #     instance.save()
    if instance.notify_user:
        print("notify users - 通知用戶!!!")
        instance.notify_user = False
        # celery worker task -> offload -> Time & task 2 cfe.sh 芹菜工人任務->卸載
        instance.notify_user_timestamp = timezone.now()
        instance.save()
# post_save.connect(name_save, sender=Product)

# 20210331 Defining and sending signals 發送信號 添加 pre_save & post_save or pre_del & post_del 等 https://docs.djangoproject.com/en/3.1/ref/signals信號/
# 預保存，到預刪除
@receiver(pre_delete, sender=BlogPost)
def blog_post_pre_delete(sender, instance, *args, **kwargs):
    # move or make a backup of this data 移動或備份此數據
    print(f"{instance.id} will be removed")

# pre_delete.connect(blog_post_pre_delete, sender=Product) 可以運用此調用連結

# 如果因某種原因而不希望要刪除您的帖子，您可以製作一個完整的其他模型。即使是相同的博客文章模型，
# 發布保存，到發布刪除
@receiver(post_delete, sender=BlogPost)
def blog_post_post_delete(sender, instance, *args, **kwargs):
    #  celery worker task -> offload -> Time & Tasks 2 cfe.sh => ＃celery worker任務->卸載-> 時間＆任務 2 cfe.sh
    print(f"{instance.id} has removed")

# post_delete.connect(blog_post_post_delete, sender=Product)

@receiver(m2m_changed, sender=BlogPost.liked.through)
def blog_post_liked_changed(sender, instance, action, *args, **kwargs):
    # print(args, kwargs) 檢測出他會抓到那些東西 (m2m_changed : https://docs.djangoproject.com/en/3.1/ref/signals/)
    # pre_add(預先廣告)用於預先添加到該字段並發布於將該字段添加到該字段中，就像發布保存預先保存一樣。
    # print(action)
    if action == 'pre_add':
        print("was added")
        qs = kwargs.get("model").objects.filter(pk__in=kwargs.get('pk_set'))
        print(qs.count())
# m2m_changed.connect(blog_post_liked_changed, sender=Product.name.through) :: https://docs.djangoproject.com/en/3.1/ref/signals/

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

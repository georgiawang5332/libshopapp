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
    # m2m_changed,
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
@receiver(pre_delete, sender=Product)
def blog_post_pre_delete(sender, instance, *args, **kwargs):
    # move or make a backup of this data 移動或備份此數據
    print(f"{instance.id} will be removed")

# pre_delete.connect(blog_post_pre_delete, sender=Product) 可以運用此調用連結

# 如果因某種原因而不希望要刪除您的帖子，您可以製作一個完整的其他模型。即使是相同的博客文章模型，
# 發布保存，到發布刪除
@receiver(post_delete, sender=Product)
def blog_post_post_delete(sender, instance, *args, **kwargs):
    #  celery worker task -> offload -> Time & Tasks 2 cfe.sh => ＃celery worker任務->卸載-> 時間＆任務 2 cfe.sh
    print(f"{instance.id} has removed")

# post_delete.connect(blog_post_post_delete, sender=Product)

# @receiver(m2m_changed, sender=Product.name.through)
# def blog_post_liked_changed(sender, instance, action, *args, **kwargs):
#     # print(args, kwargs) 檢測出他會抓到那些東西 (m2m_changed : https://docs.djangoproject.com/en/3.1/ref/signals/)
#     # pre_add(預先廣告)用於預先添加到該字段並發布於將該字段添加到該字段中，就像發布保存預先保存一樣。
#     # print(action)
#     if action == 'pre_add':
#         print("was added")
#         qs = kwargs.get("model").objects.filter(pk__in=kwargs.get('pk_set'))
#         print(qs.count())
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

#獨立開個APP自行管理
# Django signals for beginners | How to use signals in Django : https://www.youtube.com/watch?v=W8MLlwvSS-U
# 其實這些東西就是幫忙您自動跳出數字或是亂碼讓您登入這樣，一切都轉為自動的很方便。

buyers: user -> buyer, post_save
cars  : car -> buyer, post_save vs pre_save, pre_save vs save
orders: order, m2m_changed, order->sale, post_save
sales : sale -> order, pre_delete

-buyers APP:
-Car APP:
-sales APP:

admin.py
from .models import Sale
admin.site.register(Sale)

models.py
class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.amount)

-Order APP:

Order models:
from django.db import models
from cars.models import Car

class Order(models.Model):
    name  = models.CharField(max_length=200)
    cars  = models.ManyToManyField(Car)
    total = models.PositiveImtegerField(blank=True, null=True)
    total_price = models.PositiveImtegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return str(self.name)

Order admin:
from django.contrib import admin
from cars.models import Order

admin.site.register(Order)

Order apps:
from django.apps import AppConfig

class OrdersConifig(AppConfig):
    name = 'orders'
    def ready(self):
        import orders.signals

OrdersConifig __init__:
default_app_config='orders.app.OrdersConifig'

Orders signals
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from (cars).models import Order
from (sales).models import Sale

# Order:  order, m2m_changed
@receiver(m2m_changed, sender=Order.cars.through)
def m2m_changed_cars_irder(sender, instance, action, **kwargs):
    # first
    # print('running...')
    # print(action)         #避免混淆，所以先找出action中重複性質東西讓他2選1
    total = 0
    total_price = 0
    if action == "post_add" or action == "post_remove":
        #同上，因為會有manytomanyfield多選項發生，所以要了解action中的 add or remove問題，因為有時候會改為
        # 一個有時候我想選其他台車，所以金額數量都會做更動，此時signals - m2m_changed就會幫我們解決此問題。
        for car in instance.cars.all():
            # second
            print('running...')
            print(action)
            total += 1
            total_price += car.price
        instance.total = total
        instance.total_price = total_price
        instance.save()
# Sales : order->sale, post_save
@receiver(post_save, sender=Order)
def post_save_create_or_updated_sale(sender, instance, created, update_fields, **kwargs):
    obj, _ = Sale.objects.get_or_create(order=instance) #訂單是發件人的實例銷售
    obj.amount = instance.total_price
    obj.save()#post_save 需要 obj.save()

apps.py
# 寫下我們已準備方法，在這裡我們教要導入銷售信號。# 售價會關係到sales中價位，要有關聯就得要改變添加apps產生信號signals。
class SalesConfig(AppConfig):
    name='sales'
    def ready(self):
        import sales.signals #這邊是在說明，我要開啟 signals.py 的意思，然後去創建signals.py這樣。

__init__.py
#在進入此 默認程序配置，有點像setting 配置 APP一樣操作。
default_app_config='sale.apps.SalesConfig' #轉道信號signals 開通信號

signals.py

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Sale
from orders.models import Order

@receiver(pre_delete, sender=Sale)
def pre_delete_change_active_order(sender, instance, **kwargs):
    obj = instance.order #他說是找Sale中的order ForeKey相關連的資訊。#然後還可以回到此Order活動段
    obj.active = False #然後還可以回到此Order活動段
    obj.save()
    # 所以我們一但進行銷售，刪除他，訂單就不再有效了，最後保存。
    # 參考資料Django signals for beginners | How to use signals in Django
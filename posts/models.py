from django.db import models

from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save

from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
# Model Managers & Handling Drafts
# queryset_list = Post.objects.all() -> 演變為查詢集
# queryset_list = Post.objects.create(user=user, title="some Time") -> 運用建立來給予東西
class PostManagers(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManagers, self).all() #下面意思是喬遷好 本身有覆蓋功能->覆蓋view 48行那段
        return super(PostManagers, self).filter(draft=False).filter(publish__lte=timezone.now())


# 這算是進階的把檔案歸類好分辨這樣 QWQ
def images(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s" % (instance.id, filename)
    # return "%s/%s.%s" % (instance.id, instance.id, extension)


User = settings.AUTH_USER_MODEL


class Post(models.Model):
    user = models.ForeignKey(User, default=1, db_constraint=False,
                             on_delete=models.CASCADE)  # blank=True, null=True =>默認=1
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=False, max_length=10)
    img = models.ImageField(
        upload_to=images,
        null=True, blank=True,
        height_field="height_field",
        width_field="width_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    file = models.FileField(upload_to='files', null=True, blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # Item Publish Date & Draft
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    posts = PostManagers()  # or can fix:　people  = models.Manager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})  # 改變會變成1-5-6 效果
        # return reverse('posts:detail', kwargs={'slug': self.slug})

    class Mate:
        ordering: ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    # slug = slugify(instance.title)
    # # Tesla item 1 -> "Tesla-item-1"
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    #     # slug = "%s-%s" %(slugify(instance.title), instance.id)
    #     slug = "%s-%s" %(slug, instance.id)
    #     instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)

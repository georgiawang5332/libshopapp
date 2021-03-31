from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import (
    pre_save, #那是預先保存好的，所以預先保存很像後期保存
    post_save,
)

# Create your models here.

# test 03/30/2021
User = settings.AUTH_USER_MODEL

@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    before saved in the database
    """
    # print(args, kwargs)
    print(instance.username, instance.id) #None
#     trigger pre_save
#     instance.save() # <-- DONT DO　THIS -> 加了save 就出現錯誤但是可以單一加入pre_save and post_save 2選1
#     trigger post_save

# pre_save.connect(user_pre_save_receiver, sender=User)

@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    # print(args, kwargs)
    if created:
        print('send email to ', instance.username)
        # trigger(觸發板機) pre_save
        # instance.save() 加了save 就出現錯誤但是可以單一加入pre_save and post_save 2選1
        # trigger post_save
    else:
        print(instance.username, 'was just saved!!!')

# pre_save.connect(user_pre_save_receiver, sender=User)

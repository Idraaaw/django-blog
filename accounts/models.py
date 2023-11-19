from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=20,verbose_name='姓氏',null=True,blank=True)
    last_name = models.CharField(max_length=20,verbose_name='名字',null=True,blank=True)
    followers = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    

    def is_following(self, user):
        return user in self.followers.all()
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile',verbose_name='other Details', on_delete=models.CASCADE)
    bg_image = models.ImageField(upload_to='bgimage',verbose_name='网页背景图片',null=True,blank=True)
    pic = models.ImageField(upload_to='profile photo',verbose_name='头像',null=True,blank=True)
    website = models.URLField(verbose_name='网站',null=True,blank=True)
    github = models.URLField(null=True,blank=True)
    bilibili = models.URLField(verbose_name='哔哩哔哩',null=True,blank=True)
    qq = models.CharField(verbose_name='企鹅',max_length=30,null=True,blank=True)
    wechat = models.URLField(verbose_name='微信',null=True,blank=True)
    words = models.TextField(max_length=1024,null=True,blank=True)
    is_apply_followers = models.BooleanField(default=False)

    class Meta:
        verbose_name = '用户画像'
        verbose_name_plural = '用户画像'

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save,sender=User)
def create_profile(sender,**kw):
    if kw['created']:
        user_profile = UserProfile.objects.get_or_create(
            user = kw['instance']
        )
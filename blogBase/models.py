from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

import uuid

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='articles')
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=100,verbose_name='标题')
    pic = models.ImageField(upload_to='cover',blank=True)
    release_date = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    content = MarkdownxField(max_length=4096,blank=True,verbose_name='内容')
    tags = models.ManyToManyField(Tag,verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = "文章"

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    def __str__(self):
        return f"{self.user.username}'s article about {self.title}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    text = MarkdownxField(max_length=1024)
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = '评论'

    def __str__(self):
        return f"{self.user.username}对{self.article.title}的评论"

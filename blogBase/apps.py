from django.apps import AppConfig


class BlogbaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogBase'

    verbose_name = '博客管理'

from django.urls import path

from . import views

app_name = 'blogBase'
urlpatterns = [
    path('',views.index,name='index'),
    path('article/',views.view_article_list,name='view_article_list'),
    path('article/<str:id>',views.view_article,name='view_article'),
    path('portfolio/',views.view_portfolio,name='view_portfolio'),
    path('comments/add/<id>',views.add_comment,name='add_comment'),
]

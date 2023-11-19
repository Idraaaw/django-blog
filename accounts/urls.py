from django.urls import path,include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('',include('django.contrib.auth.urls'),name='login'),
    path('register/', views.register, name='register'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('view_profile/<username>',views.profile,name='view_profile'),
    path('friends/',views.friends,name='friends'),
    path('apply_join_friends/<username>',views.apply_join_friends,name='apply_join_friends'),
]
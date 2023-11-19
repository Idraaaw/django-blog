from django.contrib import admin
from django.utils.html import format_html

from .models import UserProfile,User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name')
    filter_horizontal = ('followers',)
    search_fields = ['username','email']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','words','website','github','qq','wechat','bilibili','is_apply_followers')
    list_editable = ('is_apply_followers',)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]
    list_display = UserAdmin.list_display + ('follow_info',) # 增加一列显示follow按钮
    actions = ['follow_user','unfollow_user']

    def follow_info(self,obj):
        if obj.is_superuser:
            return 'N/A'
        user_profile = UserProfile.objects.get_or_create(user=obj)[0]
        superuser = User.objects.get_or_create(is_superuser=True)[0]
        followers = superuser.followers.all()
        if user_profile.is_apply_followers:
            return 'Following'
        elif obj in followers:
            return 'Followed'
        else:
            return 'N/A'
        
    follow_info.short_description = 'Follow' # 自定义表头名
    follow_info.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']  # 移除默认的删除动作，避免误操作
        return actions

    def follow_user(self,requets,queryset):
        superuser = User.objects.get_or_create(is_superuser=True)[0]
        for user in queryset:
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
            if user_profile.is_apply_followers:
                superuser.followers.add(user)
                user_profile.is_apply_followers = False
                user_profile.save()
                superuser.save()

    follow_user.short_description = 'Follow Superuser'

    def unfollow_user(self,request,queryset):
        superuser = User.objects.get_or_create(is_superuser=True)[0]
        for user in queryset:
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
            superuser.followers.remove(user)
            superuser.save()

    unfollow_user.short_description = 'Unfollow Superuser'

    



# Register your models here.

# admin.site.register(User,UserAdmin)
# admin.site.register(UserProfile,UserProfileAdmin)
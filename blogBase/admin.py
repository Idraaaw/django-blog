from django.contrib import admin
from django.http.request import HttpRequest
from markdownx.admin import MarkdownxModelAdmin
from .models import Article,Comment,Tag

admin.site.site_header = 'IdraaawBlog管理后台'
admin.site.site_title = 'IdraaawBlog管理后台'
admin.site.index_title = 'IdraaawBlog管理后台'

class CommentListInline(admin.TabularInline):
    model = Comment
    fk = 'article'
    readonly_fields = ('user','text',)
    can_delete = True

    def has_add_permission(self, request,obj=None):
        return False


@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('id','title','release_date','display_tags',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
    autocomplete_fields = ['user']
    search_fields = ['title']
    ordering = ('-release_date',)

    inlines = [
        CommentListInline,
    ]

    def display_tags(self,obj):
        tags = obj.tags.all()
        return ','.join([tag.name for tag in tags]) if tags else 'No Tags'
    
    display_tags.short_description = '标签'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','user','text')
    list_filter = ('article','user')
    autocomplete_fields = ['user','article']

# Register your models here.
admin.site.register(Tag)

from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.functions import TruncYear
from django.db.models import Count

from .models import Article,Comment,Tag
from .forms import CommentForm

User = get_user_model()

# Create your views here.
def index(request):
    ''' 主页 '''
    superuser = User.objects.get(is_superuser=True)
    return render(request,'blogBase/index.html',{'user':superuser})

def file_article(request,tag_id):
    ''' 文章归档 '''
    tag = Tag.objects.get(pk=tag_id)
    articles = Article.objects.filter(tags=tag)
    context = {
        'tag' : tag,
        'articles' : articles,
    }
    return render(request,'blogBase/pigeonhole.html',context)

def view_article_list(request):
    ''' 显示文章列表 '''
    page = request.GET.get('page')
    tag_id = request.GET.get('tag_id')
    year = request.GET.get('year')
    context = {}
    if tag_id:
        tag_id = Tag.objects.get(pk=tag_id)
        queryset = Article.objects.filter(tags=tag_id).order_by('-release_date')
        context.update({
            'tag_id' : tag_id,
        }) 
    elif year:
        queryset = Article.objects.filter(release_date__year=year).order_by('-release_date')
        context.update({
            'year' : year,
        })
    else:
        queryset = Article.objects.all().order_by('-release_date')
    paginator = Paginator(queryset,5)
    page = page
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False
    articles_by_year = Article.objects.annotate(year=TruncYear('release_date')).values('year').annotate(count=Count('id')).order_by('-year')
    tags = Tag.objects.all()
    dict = {
        'page_obj' : page_obj,
        'is_paginated' : is_paginated,
        'articles_by_year' : articles_by_year,
        'tags' : tags,
    }
    context.update(dict)
    return render(request,'blogBase/article_list.html',context)

def view_article(request,id):
    ''' 显示具体文章详情 '''
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article' : article,
        'form' : form,
    }
    return render(request,'blogBase/article.html',context)

def view_portfolio(request):
    ''' 显示作品集 '''
    return render(request,'blogBase/portfolio.html')

@login_required
@require_POST
def add_comment(request,id):
    ''' 评论 '''
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(Article.objects.get(id=id),request.user)
    return redirect(reverse('blogBase:view_article',args=[id,]))
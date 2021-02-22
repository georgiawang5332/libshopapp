from urllib.parse import quote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Post
from .forms import PostForms

# Create your views here.

def posts_create(request):  # retrieve
    # basic use permissions 基本使用權限; 添加這個但是在無痕中會出現404
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated:
    #     raise Http404

    form = PostForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # Associate User to Post with a Foreign Key #關聯用戶以外鍵進行發布
        # instance.user = request.user
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully Created")
    context = {
        'form': form,
    }
    return render(request, 'posts/post_form.html', context)

def posts_detail(request, id=None):  # retrieve
    instance = get_object_or_404(Post, id=id)
    # instance = get_object_or_404(Post, slug=slug)
    # 這要強調是 工作人員可子看見 "草稿" 非工作人員或是超級用戶會排除 我就不用擔心
    # if instance.draft: #出現草稿就這樣填上 下面是日期可以了解下
    if instance.publish > timezone.now() or instance.draft: #填上一些日期部分做區分
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
    }
    return render(request, 'posts/post_detail.html', context)

# from operator import attrgetter
# def home_screen_view(request):
#     context = {}
#     query = ""
#     if request.GET:
#         query = request.GET['q']
#         context['query'] = str(query)
#     list_posts = sorted(posts_list(query), key=attrgetter('date_updated'), reverse=True)
#     context['list_posts'] = list_posts
#     return render(request, "posts/post_list.html", context)

# paginator / odel Managers & Handling Drafts /
def posts_list(request):  # list items
    # Manager 管理員類型觀看 (選擇隱藏或是公開草稿)
    today = timezone.now().date()
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #.all() #.order_by("-timestamp") 運用filter意思是未來文章/草稿不會出現 -> Model Managers & Handling Drafts
    queryset_list = Post.posts.active() #.order_by("-timestamp") 運用filter意思是未來文章/草稿不會出現 -> Model Managers & Handling Drafts
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.posts.all()

    # search 搜索list內資訊
    query = request.GET.get("q") #.split(" ")# python install 2020 => [python, install, 2020]
    if query:
        queryset_list = queryset_list.filter(
            # title__icontains=query)
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(timestamp__icontains=query)
            # Q(user_id__first_name__icontains=query) |
        ).distinct()

    # paginator 分頁
    # paginator = Paginator(queryset_list, 35)  # Show 25 contacts per page.

    # page_reguest_var = "page"
    # page = request.GET.get(page_reguest_var)
    #
    # try:
    #     queryset = paginator.page(page)
    # except PageNotAnInteger:
    #     #     if page is not an intrger, deliver first page.
    #     queryset = paginator.page(1)
    # except EmptyPage:
    #     #     if page out of range(e.g. 9999), deliver last page of request
    #     queryset = paginator.page(paginator.num_pages)

    context = {
        # 'object_list': queryset,
        # 'title': 'List',
        # 'page_reguest_var': page_reguest_var,
        # 'today': today,
    }
    return render(request, 'posts/post_list.html', context)

def posts_update(request, id=None):
    # basic use permissions 基本使用權限
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id) #抓出第幾個單頁
    form = PostForms(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "<a href='#>Item</a> Saved", extra_tags='html_safe')
        # messages.success(request, "Successfully Item Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'posts/post_form.html', context)

def posts_delete(request, id=None):
    # basic use permissions 基本使用權限
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "successfully deleted")
    return redirect("posts:list")

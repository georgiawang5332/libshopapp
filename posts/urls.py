from django.urls import path

from . import views

# Create your urls here.
app_name = 'posts'

urlpatterns = [
        # path('aaa/', views.aaa, name='aaa'),
        path('list', views.posts_list, name='list'),
        path('create/', views.posts_create, name='create'),
        # path('detail/<id>/', views.posts_detail, name='detail'),#http://127.0.0.1:7001/posts/detail/9/
        path('<int:id>/detail', views.posts_detail, name='detail'), #http://127.0.0.1:7001/posts/9/
        # path('update/', views.posts_update, name='update'),
        path('<int:id>/update/', views.posts_update, name='update'),#http://127.0.0.1:7001/posts/3/edit/
        path('<int:id>/delete/', views.posts_delete, name='delete'),
    ]
from django.urls import path

from . import views

# Create your urls here.
app_name = 'posts'

urlpatterns = [
        # path('aaa/', views.aaa, name='aaa'),
        path('list', views.posts_list, name='list'),#http://127.0.0.1:8000/posts/list
        path('create/', views.posts_create, name='create'),#http://127.0.0.1:8000/posts/create
        path('<int:id>/detail', views.posts_detail, name='detail'), #http://127.0.0.1:8000/posts/9/
        path('<int:id>/update/', views.posts_update, name='update'),#http://127.0.0.1:8000/posts/3/edit/
        path('<int:id>/delete/', views.posts_delete, name='delete'),#http://127.0.0.1:8000/posts/delete
    ]
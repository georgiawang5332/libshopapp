"""libshopapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views
from home.views import secretPage

urlpatterns = [
    path('store/', include('store.urls', namespace='store')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('', include('home.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# app_name # 後台

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls'), name='auth'),
    path('accounts/', include('django.contrib.auth.urls'), name='register'),
    # path('accounts/', include('accounts.urls')),  # new 20210323

                   # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
                   # 參考資料: https://github.com/mitchtabian/CodingWithMitch-Blog-Course/blob/Reset-Password-and-Change-Password-(Django)/src/mysite/urls.py
                   path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
                   path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

                   path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),  # 寫信箱郵件
                   path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),#我們已通過電子郵件發送給您有關設置密碼的說明。 如果幾分鐘後還沒到達，請檢查您的垃圾郵件文件夾。
                   path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
                        name='password_reset_confirm'),
                   path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),#密碼已更改！
                   # path("secretPage/", views.secretPage.as_view(), name="secretPage"),  # 20210408

               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

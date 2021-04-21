from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Create your urls here.
app_name = 'home'

urlpatterns = [
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name="home/change_password.html",
            success_url='/'
        ),  
        name="change_password"
    ),# 20210415
    # path("secretPage/", views.secretPage, name="secretPage"),  #20210408
    path("register/", views.register, name="register"),  # 20210325
    path('social/', views.socialview, name='social'),
    path('about/', views.aboutview, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
]

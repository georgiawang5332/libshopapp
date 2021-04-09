from django.urls import path
from . import views

# Create your urls here.
app_name = 'home'

urlpatterns = [
    path("secretPage/", views.secretPage, name="secretPage"),  #20210408
    path("register/", views.register, name="register"), #20210325
    path('social/', views.socialview, name='social'),
    path('about/', views.aboutview, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
]

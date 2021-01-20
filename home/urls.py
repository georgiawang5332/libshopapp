from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # path('order/', views.order, name='order'),
    path('social/', views.socialview, name='social'),
    path('about/', views.aboutview, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
]

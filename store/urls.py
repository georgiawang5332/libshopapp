from django.urls import path
from . import views

# Create your urls here.
# http://127.0.0.1:8000/accounts/logout/
app_name = 'store'

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),

    path('create/', views.productCreate, name='create'),
    path('<int:id>/', views.productDetail, name='detail'),
    path('<int:id>/update/', views.productUpdate, name='update'),
    # path('changePassword/', views.changePassword, name='changePassword'),
    path('<int:id>/delete/', views.productDelete, name='delete'),

    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name='update_item'),
    # path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('searchbar/', views.searchbar, name='searchbar'),




]

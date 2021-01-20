from django.contrib import admin
from store.models import *

# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'price', 'digital', 'image', "updated", "timestamp"]
    search_fields = ["name", "content"]
    list_display_links = ["updated"]
    list_editable = ["name"]
    list_filter = ["updated", "timestamp"]

    class Meta:
        model = Product

admin.site.register(Customer)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
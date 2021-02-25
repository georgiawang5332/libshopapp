from django.contrib import admin
from store.models import *

# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content', 'price', 'draft', 'digital', 'image', "updated", "timestamp"]
    list_display_links = ["content"]
    list_editable = ["name"]
    search_fields = ["name", "content"]
    list_filter = ["updated", "timestamp"]

    class Meta:
        model = Product

admin.site.register(Customer)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
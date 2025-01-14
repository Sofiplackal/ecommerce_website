from django.contrib import admin
from .models import Customer, Order, OrderItem, ShippingAddress, Product, Wishlist

# Register the models
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

#Product Admin Configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')  # Display these fields in the admin list view
    search_fields = ('user__username', 'product__name')  # Add search functionality for these fields
    list_filter = ('user',)  # Add filtering options by user












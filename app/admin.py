from django.contrib import admin

# Register your models here.

from .models import Product
from .models import Profile

class ProductAdmin(admin.ModelAdmin):
	list_display=('product_name','price','supermarket',)

class ProfileAdmin(admin.ModelAdmin):
	list_display=('user',)

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Product,ProductAdmin)
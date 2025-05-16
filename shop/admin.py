from django.contrib import admin
from .models  import *

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','product_image','description')
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','profile_picture','userid')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
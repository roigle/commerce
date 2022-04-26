from django.contrib import admin

from .models import User, Category, Product, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user_id", "price", "current_bid", "status", "category", "image", "description")

class BidAdmin(admin.ModelAdmin):
    list_display = ("user_id", "product_id", "bid")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_id", "product_id", "comment")


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
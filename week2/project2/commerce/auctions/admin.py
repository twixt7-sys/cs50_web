from django.contrib import admin

from .models import User, Listing, Bid, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("name", "highest_bid")
    
class BidAdmin(admin.ModelAdmin):
    list_display = ("amount", "bidder")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "listing")

models = (
    (User, UserAdmin),
    (Listing, ListingAdmin),
    (Bid, BidAdmin),
    (Comment, CommentAdmin)
    )

for model, display in models:
    admin.site.register(model, display)


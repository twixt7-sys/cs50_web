from django.contrib import admin

from .models import User, Listing, Bid, Comment

for model in [User, Listing, Bid, Comment]:
    admin.site.register(model)

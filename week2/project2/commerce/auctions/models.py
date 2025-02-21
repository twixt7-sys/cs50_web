from django.contrib.auth.models import AbstractUser
from django.db import models as m

class User(AbstractUser):
    id = m.AutoField(primary_key=True)
    watchlist = m.ManyToManyField("Listing", blank=True, related_name="watchers")
    username = m.CharField(max_length=150, unique=True)
    password = m.CharField(max_length=128)
    email = m.EmailField(max_length=254, unique=True)
    
    def __str__(self):
        return f"username: {self.username}\nemail: {self.email}\npassword: {self.password}"

class Listing(m.Model):
    id = m.AutoField(primary_key=True)
    is_active = m.BooleanField(default=True)    
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name="Listings")
    name = m.CharField(max_length=150)
    price = m.DecimalField(max_digits=10, decimal_places=2)
    description = m.TextField()
    date = m.DateTimeField(auto_now_add=True)
    image_url = m.URLField(null=True, blank=True)
    category = m.CharField(max_length=150, null=True, blank=True)

class Bid(m.Model): # fields: amount, bidder, listing
    amount = m.DecimalField(max_digits=10, decimal_places=2)
    bidder = m.ForeignKey(User, on_delete=m.CASCADE, related_name="bids")
    listing = m.ForeignKey(Listing, on_delete=m.CASCADE, related_name="bids")

class Comment(m.Model): # fields: content, commenter, listing
    content = m.TextField()
    commenter = m.ForeignKey(User, on_delete=m.CASCADE, related_name="comments")
    listing = m.ForeignKey(Listing, on_delete=m.CASCADE, related_name="comments")
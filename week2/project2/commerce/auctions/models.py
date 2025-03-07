from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.utils import timezone

class User(AbstractUser):
    watchlist = m.ManyToManyField("Listing", blank=True, related_name="watchers")
    
    def __str__(self):
        return f"username: {self.username}, email: {self.email}"

class Listing(m.Model):
    is_active = m.BooleanField(default=True)    
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name="listings")
    name = m.CharField(max_length=150)
    price = m.DecimalField(max_digits=10, decimal_places=2)
    description = m.TextField()
    date = m.DateTimeField(auto_now_add=True)
    image_url = m.URLField(null=True, blank=True)
    category = m.CharField(max_length=150, null=True, blank=True)
    starting_bid = m.ForeignKey('Bid', null=True, blank=True, on_delete=m.SET_NULL, related_name="starting_for")  
    highest_bid = m.ForeignKey('Bid', null=True, blank=True, on_delete=m.SET_NULL, related_name="highest_for")
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only applies when creating a new Listing
            super().save(*args, **kwargs)  # Save first to get an ID
            if not self.starting_bid:
                default_bid = Bid.objects.create(amount=0, bidder=self.user, listing=self)
                self.starting_bid = default_bid
        super().save(*args, **kwargs)  # Save again with the starting_bid set
    
    def __str__(self):
        return self.name

class Bid(m.Model):
    amount = m.DecimalField(max_digits=10, decimal_places=2)
    bidder = m.ForeignKey(User, on_delete=m.CASCADE, related_name="bids")
    listing = m.ForeignKey(Listing, on_delete=m.CASCADE, related_name="bids")
    timestamp = m.DateTimeField(default=timezone.now)  # Set default to current time

    def __str__(self):
        return f"{self.bidder.username} bid {self.amount} on {self.listing.name}"
    
class Comment(m.Model):
    content = m.TextField()
    commenter = m.ForeignKey(User, on_delete=m.CASCADE, related_name="user_comments")
    listing = m.ForeignKey(Listing, on_delete=m.CASCADE, related_name="listing_comments")
    created_at = m.DateTimeField(default=timezone.now)  # Use current time as default

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.listing.name}"
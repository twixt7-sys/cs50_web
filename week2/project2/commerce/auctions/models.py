from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.utils import timezone

class User(AbstractUser):
    watchlist = m.ManyToManyField("Listing", blank=True, related_name="watchers")
    
    def __str__(self):
        return f"username: {self.username}, email: {self.email}"

class Listing(m.Model):
    id = m.AutoField(primary_key=True)
    is_active = m.BooleanField(default=True)    
    user = m.ForeignKey(User, on_delete=m.CASCADE, related_name="listings")
    name = m.CharField(max_length=150)
    description = m.TextField()
    date = m.DateTimeField(auto_now_add=True)
    image_url = m.URLField(null=True, blank=True)
    category = m.CharField(max_length=150, null=True, blank=True)
    starting_bid = m.ForeignKey('Bid', null=True, blank=True, on_delete=m.SET_NULL, related_name="starting_for")  
    highest_bid = m.ForeignKey('Bid', null=True, blank=True, on_delete=m.SET_NULL, related_name="highest_for")
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the instance is new
        super().save(*args, **kwargs)  # First save to get a primary key

        if is_new and not self.starting_bid:
            default_bid = Bid.objects.create(amount=0, bidder=self.user, listing=self)
            Listing.objects.filter(pk=self.pk).update(starting_bid=default_bid, highest_bid=default_bid)



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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    active_listings = [listing for listing in listings if listing.is_active]
    return render(request, "auctions/index.html", {
        "user": request.user,
        "active_listings": active_listings
    })

def login_view(request):
    if request.method == "POST":
        username, password  = request.POST["username"], request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    #using a dictionary for more dynamacity
    labels = ["name", "description", "start_bid", "image_url", "category"]
    data = [
        {
            "label": field.replace("_", " ").title() + ":",
            "type": "number" if "bid" in field else "url" if "image" in field else "text",
            "name": field,
            "placeholder": field.replace("_", " ").title(),
        }
        for field in labels
    ]
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "save":
            if request.user.is_authenticated:
                Listing.objects.create(
                    user = request.user,
                    name = request.POST.get("name"),
                    description = request.POST.get("description"),
                    image_url = request.POST.get("image_url"),
                    category = request.POST.get("category"),
                )
                return redirect("index")
            else:
                return redirect("login")
        
        elif action == "cancel":
            return redirect("index")
    
    return render(request, "auctions/create.html", {"data": data})

def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user = request.user
    
    # Ensure starting_bid exists
    if listing.starting_bid is None:
        listing.starting_bid = Bid.objects.create(amount=0, bidder=listing.user, listing=listing)
        listing.save()
    
    highest_bid_amount = listing.highest_bid.amount if listing.highest_bid else 0
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "Add to Watchlist":
            user.watchlist.add(listing)
        elif action == "Remove from Watchlist":
            user.watchlist.remove(listing)
        elif action == "Comment":
            comment_text = request.POST.get("comment")
            if comment_text:
                Comment.objects.create(
                    content=comment_text,
                    commenter=user,
                    listing=listing,
                )
            return redirect("listing", listing_id=listing_id)
        elif action == "Place Bid":
            try:
                bid_amount = float(request.POST.get("bid", 0))
            except ValueError:
                messages.error(request, "Invalid bid amount.")
                return redirect("listing", listing_id=listing_id)
            
            if bid_amount <= listing.starting_bid.amount or (listing.highest_bid and bid_amount <= highest_bid_amount):
                is_error = True
                message = "Your bid must be higher than the starting bid and the current highest bid."
            else:
                new_bid = Bid.objects.create(amount=bid_amount, bidder=user, listing=listing)
                listing.highest_bid = new_bid
                listing.save()
                is_error = False
                message = "Bid placed successfully."
            return render(request, "auctions/listing.html", {
                "is_error": is_error,
                "message": message,
                "user": user,
                "listing": listing,
                "display": {
                    "Item ID": listing.id,
                    "Uploaded by": listing.user.username,
                    "Category": listing.category,
                    "Date added": listing.date
                }
            })
        elif action == "Close Bid":
            listing.is_active = False
            listing.save()
            return redirect("listing", listing_id=listing_id)
        elif action == "Open Bid":
            listing.is_active = True
            listing.save()
            return redirect("listing", listing_id=listing_id)
    
    display = {
            "Item ID": listing.id,
            "Uploaded by": listing.user.username,
            "Category": listing.category,
            "Date added": listing.date
        }
    if not listing.is_active:
        display = {"Winner": listing.highest_bid.bidder.username, **display}
        
    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "display": display
    })


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "user": request.user,
        "watchlist": request.user.watchlist.all()
    })

def bid(request, listing_id):
    return render(request, "auctions/bid.html")

def categories(request):
    if request.method == "GET":
        pass
    return render(request, "auctions/categories.html")
    
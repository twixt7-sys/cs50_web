from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal

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
                    price=Decimal(request.POST.get("start_bid") or "0.00"),
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
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "Add to Watchlist":
            user.watchlist.add(listing)
        elif action == "Remove from Watchlist":
            user.watchlist.remove(listing)
        elif action == "Comment":
            comment_text = request.POST.get("comment")
            print("Commenting")
            if comment_text:
                print("Commenting")
                Comment.objects.create(
                    content=comment_text,
                    commenter=user,
                    listing=listing,
                )
        elif action == "Bid":
            pass
        elif action == "Close Bid":
            pass
    
    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "display": {
            "Item ID": listing.id,
            "Uploaded by": listing.user.username,
            "Category": listing.category,
            "Date added": listing.date
        }
    })

def watchlist(request, username):
    return render(request, "auctions/watchlist.html", {
        "user": request.user,
        "watchlist": request.user.watchlist.all()
    })

def bid(request, listing_id):
    return render(request, "auctions/bid.html")
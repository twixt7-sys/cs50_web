from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal

from .models import User, Listing


def index(request):
    listings = Listing.objects.all()
    active_listings = [listing for listing in listings if listing.is_active]
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=listing_id),
    })
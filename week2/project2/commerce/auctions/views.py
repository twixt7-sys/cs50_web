from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages

from .models import User, Listing, Bid, Comment
from .forms import CategoryForm, CreateForm


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

@login_required
def create_listing(request):
    form = CreateForm(request.POST)

    if request.method != "POST" or not form.is_valid():
        return render(request, "auctions/create.html", {"form": form})

    action = request.POST.get("action")

    if action == "enter":
        listing = Listing.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            image_url=request.POST.get("image_url"),
            category=request.POST.get("category"),
            user=request.user,
        )

        starting_bid = Bid.objects.create(
            amount=Decimal(request.POST.get("start_bid")),
            bidder=request.user,
            listing=listing,
        )

        listing.highest_bid = starting_bid
        listing.save(update_fields=["highest_bid"])

        return redirect("index")

def listing(request, listing_id):
    listing, user = get_object_or_404(Listing, id=listing_id), request.user
    highest_bid_amount = listing.highest_bid.amount if listing.highest_bid else 0
    display = {
                "Item ID": listing.id,
                "Uploaded by": listing.user.username,
                "Category": listing.category,
                "Date added": listing.date
            }
    
    if request.method != "POST":
        return render(request, "auctions/listing.html", {
            "user": user,
            "listing": listing,
            "display": display
        })
    
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
        bid_amount = float(request.POST.get("bid", 0))
        # message = (is_success, message) 
        if bid_amount <= listing.starting_bid.amount or (listing.highest_bid and bid_amount <= highest_bid_amount):
            message = (False, "Your bid must be higher than the starting bid and the current highest bid.")
            
        else:
            new_bid = Bid.objects.create(amount=bid_amount, bidder=user, listing=listing)
            listing.highest_bid = new_bid
            listing.save()
            message = (True, "Bid placed successfully.")

        return render(request, "auctions/listing.html", {
            "is_error": message[0],
            "message": message[1],
            "user": user,
            "listing": listing,
            "display": display
        })

    if action in ["Close Bid", "Open Bid"]:
        listing.is_active = (action == "Open Bid")
        listing.save()
        return redirect("listing", listing_id=listing_id)

    if not listing.is_active:
        display = {"Winner": listing.highest_bid.bidder.username, **display}
    
    return redirect("listing", listing_id=listing_id)

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "user": request.user,
        "watchlist": request.user.watchlist.all()
    })

def categories(request):
    form = CategoryForm()
    query = request.GET.get('category', '').strip()
    results = [] if not query else Listing.objects.filter(category__icontains=query).distinct()

    return render(request, "auctions/categories.html", {
        "form": form,
        "results": results,
        "query": query
    })
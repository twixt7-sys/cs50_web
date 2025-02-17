from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .models import Flight, Airport, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })
    
def flight(request, flight_id): # dynamic url
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })
    
def book(request, flight_id):   #dynamic url
    r = request
    if r.method == "POST":
        # access flight
        flight = Flight.objects.get(pk=flight_id)
        # find passenger id from submitted form
        passenger_id = int(r.POST["passenger"])
        # find passenger based on id
        passenger = Passenger.objects.get(pk=passenger_id)
        # add passenger to flight
        passenger.flights.add(flight)
        
        # redirect to flight page after successful booking
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
        
        
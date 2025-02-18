from django.db import models as m

# Airport table with code and city columns
class Airport(m.Model):
    code = m.CharField(max_length=3)
    city = m.CharField(max_length=64)
    
    def __str__(self):   # toString method
        return f"{self.city} ({self.code})"

# Flight table with origin, destination, and duration columns
class Flight(m.Model):
    origin = m.ForeignKey(Airport, on_delete=m.CASCADE, related_name="departures")  #refer to flights that leave from an airport location
    destination = m.ForeignKey(Airport, on_delete=m.CASCADE, related_name="arrivals")    # refer to flights that arrive from an airport location
    duration = m.IntegerField()
    
    def __str__(self):  # toString method
        return f"{self.id}: {self.origin} to {self.destination}"

class Passenger(m.Model):
    #fields
    first = m.CharField(max_length=64)
    last = m.CharField(max_length=64)
    flights = m.ManyToManyField(Flight, blank=True, related_name="passengers")
    
    def __str__(self):
        return f"{self.first} {self.last}"
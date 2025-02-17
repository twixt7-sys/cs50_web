from django.contrib import admin

from.models import Flight, Airport, Passenger

class FlightAdmin(admin.ModelAdmin):
    list_display  = ("id", "origin", "destination", "duration")

# Register your models here. (appears in the admin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Airport)
admin.site.register(Passenger)


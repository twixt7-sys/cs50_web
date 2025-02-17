from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:flight_id>', views.flight, name="flight"),
    path('<str:flight_id>/book', views.book, name="book")
]
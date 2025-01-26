from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index.html"),
    path("trisha", views.trisha, name="trisha"),
    path("luke", views.luke, name="luke"),
    path("greet/<str:name>", views.greet, name="greet")
]

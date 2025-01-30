from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

app_name = "tasks"

tasks = ["foo", "bar", "baz"]

# Create your views here.
def index(request):
    return render(request, "tasks/index.html", {
        "tasks": tasks
    })
    
def add(request):
    #validatinf form data
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            tasks.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))            
        else:
            form = NewTaskForm() # if invalid, re-render form

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
    
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
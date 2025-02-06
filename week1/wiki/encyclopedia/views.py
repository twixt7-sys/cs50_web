from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from . import util

import markdown2 as md2
import random as r


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All Pages"
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "error": "The page you are looking for does not exist."
        })
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title,
        "content": md2.markdown(entry)
    })
    
def search(request):
    query = request.GET.get('q', '')    #the empty string sets a default value for the query 
    if query:
        #execute logic for search
        entries = util.list_entries()
        # iterates over the entries list and filteres out only the entries that contain the query (lower or uppercase) 
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "results": [],
            "query": query
        })

def newpage(request):
    if request.method == "POST":
        # get the needed data from the form
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        
        # check if the title already exists
        if new_title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error": "The page you are trying to create already exists."
            })
        else:
            # save the new page
            util.save_entry(new_title, new_content)
            entry = util.get_entry(new_title)
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "title": new_title,
                "content": md2.markdown(entry)
            })
    else:
        return render(request, "encyclopedia/newpage.html")

def edit(request, title):
    entry = util.get_entry(title)
    
    if request.method == "POST":
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        util.save_entry(new_title, new_content)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": new_title,
            "content": md2.markdown(entry)
        })
    
    if entry is None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "title": title,
        "content": entry
    })
    
def random(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "error": "No entries available."
        })
    random_title = r.choice(entries)
    entry = util.get_entry(random_title)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": random_title,
        "content": md2.markdown(entry)
    })
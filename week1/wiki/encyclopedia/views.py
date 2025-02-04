from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "All Pages"
    })

def entry(request, title):
    
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "error": "The page you are looking for does not exist."
        })
    
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "content": markdown2.markdown(util.get_entry(title))
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
            "results": [],  #return results as an empty list if no query is provided
            "query": query
        })

def newpage(request):
    if request.method == "POST":
        # get the needed data from the form
        title = request.POST.get("title")   #get the title from the form
        content = request.POST.get("content")   #get the content from the form
        
        # check if the title already exists
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error": "The page you are trying to create already exists."
            })
        else:
            # save the new page
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/newpage.html")
        
def edit(request, title):
    if request.method == "POST":
        # get the needed data from the form
        new_title = request.POST.get("title")
        content = request.POST.get("content")
        
        # validate the form data
        if not new_title or not content:
            return HttpResponseBadRequest("Title and content cannot be empty.")
        
        # save the edited page
        util.save_entry(new_title, content)
        
        
        return redirect('entry', title=new_title)
    else:
        # get the current content of the page
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })



from django.shortcuts import render

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
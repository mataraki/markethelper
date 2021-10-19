from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util


def createpage(request):
    if request.method == "POST":
        newtitle = request.POST['createdtitle']
        if util.get_entry(newtitle) != None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists"
            })
        else: 
            util.save_entry(newtitle, bytes(request.POST['createdtext'], 'utf8'))
            return HttpResponseRedirect(f"/wiki/{newtitle}")
    else:
        #if page loads via search form
        searchq = request.GET.get("q")
        if searchq:
            return HttpResponseRedirect(f"/?q={searchq}")
        #if page loads via typing or clicking the link
        else:
            return render(request, "encyclopedia/create.html")

def index(request):
    #if page loads via search form
    searchq = request.GET.get("q")
    if searchq:
        if util.get_entry(searchq) != None:
            return HttpResponseRedirect(f"/wiki/{searchq}")
        else:
            searchresults = []
            for entry in util.list_entries():
                if searchq in entry:
                    searchresults.append(entry)
            if len(searchresults) > 0:
                return render(request, "encyclopedia/search.html", {
                    "entries": searchresults
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No results found"
                })
    #if page loads via typing or clicking the link
    else: return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def editpage(request, title):
    if request.method == "POST":
        util.save_entry(title, bytes(request.POST['edited'], 'utf8'))
        return HttpResponseRedirect(f"/wiki/{title}")
    else:
        #if page loads via search form
        searchq = request.GET.get("q")
        if searchq:
            return HttpResponseRedirect(f"/?q={searchq}")
        #if page loads via typing or clicking the link
        else:
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/edit.html", {
                    "entry": util.get_entry(title),
                    "title": title
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "Requested page was not found"
                })

def entrypage(request, title):
    #if page loads via search form
    searchq = request.GET.get("q")
    if searchq:
        return HttpResponseRedirect(f"/?q={searchq}")
    #if page loads via typing or clicking the link
    else:
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/entrypage.html", {
                "title": title,
                "entry": markdown2.markdown(util.get_entry(title))
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Requested page was not found"
            })

def randompage(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{title}")
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.fields import DecimalField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home",
    "Toys"
]


def index(request):
    if request.user.is_authenticated:
        watchings = len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
    else:
        watchings = None
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(isopen=False).all(),
        "watchings": watchings
    })


@login_required
def bid(request, id):
    lf = Listing.objects.filter(id=id)
    lg = Listing.objects.get(id=id)
    bf = Bid.objects.filter(listing=lg)
    if len(bf) > 0:
        bg = Bid.objects.get(listing=lg)
        if float(request.POST["bid"]) > bg.price:
            bf.update(user=request.user, price=request.POST["bid"], bidcount=(bg.bidcount + 1))
            lf.update(price=request.POST["bid"])
            request.session['message'] = 'Bid placed'
            return HttpResponseRedirect(reverse("listings", args=(id,)))
        else:
            request.session['message'] = 'Insufficient bid price'
            return HttpResponseRedirect(reverse("listings", args=(id,)))
    else:
        if float(request.POST["bid"]) >= lg.price:
            bc = Bid.objects.create(user=request.user, listing=Listing.objects.get(id=id), price=request.POST["bid"], bidcount=1)
            lf.update(price=request.POST["bid"])
            request.session['message'] = 'Bid placed'
            return HttpResponseRedirect(reverse("listings", args=(id,)))
        else:
            request.session['message'] = 'Insufficient bid price'
            return HttpResponseRedirect(reverse("listings", args=(id,)))



def categoriespage(request):
    if request.user.is_authenticated:
        watchings = len(User.objects.get(username = request.user).watchings.all())
    else:
        watchings = None
    return render(request, 'auctions/categories.html', {
        "categories": CATEGORIES,
        "watchings": watchings
    })


def categorypage(request, category):
    if request.user.is_authenticated:
        watchings = len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
    else:
        watchings = None
    if category.capitalize() in CATEGORIES:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(category=category.capitalize()).exclude(isopen=False),
            "header": "from " + category.capitalize() + " category",
            "watchings": watchings
        })
    else:
        return render(request, 'auctions/categories.html', {
            "categories": CATEGORIES,
            "watchings": watchings
        })


@login_required
def close(request, id):
    lf = Listing.objects.filter(id=id)
    lg = Listing.objects.get(id=id)
    bf = Bid.objects.filter(listing=lg)
    if len(bf) > 0:
        bg = Bid.objects.get(listing=Listing.objects.get(id=id))
        bidwinner = str(bg.user)
    else: 
        bidwinner = "No one"
    lf.update(isopen=False, winner=bidwinner)
    return HttpResponseRedirect(reverse("listings", args=(id,)))


@login_required
def create(request):
    # Via POST (creating item)
    if request.method == "POST":

        # Collect new listing info
        user = request.user
        title = request.POST["title"]
        try:
            description = request.POST["description"]
        except KeyError:
            description = ""
        startprice = request.POST["startprice"]
        photo = request.POST["photo"]
        try:
            category = request.POST["category"]
        except KeyError:
            category = "No Category Listed"

        # Check if info is correct
        if title is None:
            return render(request, "auctions/create.html", {
                "message": "Must provide title.",
                "categories": CATEGORIES,
                "watchings": len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
            })
        if description is None:
            return render(request, "auctions/create.html", {
                "message": "Must provide description.",
                "categories": CATEGORIES,
                "watchings": len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
            })
        try:    
            val = float(startprice) 
        except ValueError:    
            return render(request, "auctions/create.html", {
                "message": "Must provide valid price.",
                "categories": CATEGORIES,
                "watchings": len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
            })
        else:
            l = Listing.objects.create(user=user, title=title, description=description, price=startprice, photo=photo, category=category)
            return HttpResponseRedirect(reverse("index"))
    # Via GET (visiting page)
    else:
        return render(request, "auctions/create.html", {
            "categories": CATEGORIES,
            "watchings": len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
        })


@login_required
def comment(request, id):
    l = Comment.objects.create(user=request.user, listing=Listing.objects.get(id=id), text=request.POST["comment"])
    request.session['message'] = 'Comment added'
    return HttpResponseRedirect(reverse("listings", args=(id,)))


def listings(request, id):
    isopen = True
    loggedin = False
    owned = False
    bided = False
    watched = False
    categorized = False
    bidcount = 0
    if Listing.objects.get(id=id).isopen == False:
        isopen = False
    if request.user.is_authenticated:
        loggedin = True
        watchings = len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
    else:
        watchings = None
    if request.user == Listing.objects.get(id=id).user:
        owned = True
    b = Bid.objects.filter(listing=Listing.objects.get(id=id))
    if len(b) > 0:
        bb = Bid.objects.get(listing=Listing.objects.get(id=id))
        bidcount = bb.bidcount
        if request.user == bb.user:
                bided = True
    if request.user in Listing.objects.get(id=id).watchers.all():
        watched = True       
    if Listing.objects.get(id=id).category != "No Category Listed":
        categorized = True
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']
    else:
        message = None
        
    return render(request, "auctions/listing.html", {
        "listings": Listing.objects.filter(id=id),
        "comments": Comment.objects.filter(listing=Listing.objects.get(id=id)),
        "isopen": isopen,
        "loggedin": loggedin,
        "owned": owned,
        "bided": bided,
        "watched": watched,
        "categorized": categorized,
        "bidcount": bidcount,
        "winner": Listing.objects.get(id=id).winner,
        "watchings": watchings,
        "message": message
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def userpage(request, name):
    owner = User.objects.get(username = name)
    if request.user.is_authenticated:
        watchings = len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
    else:
        watchings = None
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(user=owner).exclude(isopen=False),
        "header": "by " + name,
        "watchings": watchings
    })


@login_required
def watch(request, id):
    lg = Listing.objects.get(id=id)
    lg.watchers.add(User.objects.get(username = request.user))
    request.session['message'] = 'Added to watchlist'
    return HttpResponseRedirect(reverse("listings", args=(id,)))


@login_required
def unwatch(request, id):
    lg = Listing.objects.get(id=id)
    lg.watchers.remove(User.objects.get(username = request.user))
    request.session['message'] = 'Removed from watchlist'
    return HttpResponseRedirect(reverse("listings", args=(id,)))


@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": User.objects.get(username = request.user).watchings.all().exclude(isopen=False),
        "watchings": len(User.objects.get(username = request.user).watchings.all().exclude(isopen=False))
    })
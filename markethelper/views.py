import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import datetime

from .models import User, Share, Event


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        return render(request, "markethelper/index.html", {
            "name": user.username,
            "invested": user.invested,
            "token": user.iextoken
        })
    else:
        return render(request, "markethelper/login.html")


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
            return render(request, "markethelper/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "markethelper/login.html")


@login_required
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
            return render(request, "markethelper/register.html", {
                "message": "Passwords must match."
            })

        # Ensure token was given and save token and starting sum
        token = request.POST["iextoken"]
        if token == "":
            return render(request, "markethelper/register.html", {
                "message": "Must provide IEX token."
            })
        
        startingsum = request.POST["startingsum"]
        if startingsum.isdecimal() == False:
            startingsum = 0

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.iextoken = token
            user.invested = startingsum
            user.save()
        except IntegrityError:
            return render(request, "markethelper/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "markethelper/register.html")


@login_required
@csrf_exempt
def deposit(request):
    deposit = Decimal(json.loads(request.body))
    user = User.objects.get(username=request.user)
    user.invested += deposit
    user.save()
    return JsonResponse({"message": "Your funds were deposited."}, status=201)


@login_required
@csrf_exempt
def buy(request):
    sharebought = json.loads(request.body)
    search = Share.objects.filter(owner=request.user, ticker=sharebought["ticker"])
    if len(search) != 0:
        share = Share.objects.get(owner=request.user, ticker=sharebought["ticker"])
        share.pricebought = (share.pricebought * share.quantity + Decimal(sharebought["price"]) * int(sharebought["quantity"])) / (share.quantity + int(sharebought["quantity"]))
        share.pricecurrent = Decimal(sharebought["price"])
        share.quantity += int(sharebought["quantity"])
        share.save()
    else:
        share = Share(
            owner = request.user,
            type = sharebought["type"].lower(),
            ticker = sharebought["ticker"].upper(),
            name = sharebought["name"],
            quantity = int(sharebought["quantity"]),
            pricebought = Decimal(sharebought["price"]),
            pricecurrent = Decimal(sharebought["price"]),
            currency = sharebought["currency"],
            rating = sharebought["rating"]
        )
        if share.name == "":
            share.name = share.ticker
        share.save()
    return JsonResponse({"message": "Shares successfully bought."}, status=201)


@login_required
@csrf_exempt
def sell(request):
    sharesold = json.loads(request.body)
    search = Share.objects.filter(owner=request.user, ticker=sharesold["ticker"])
    if len(search) != 0:
        share = Share.objects.get(owner=request.user, ticker=sharesold["ticker"])
        if share.quantity < int(sharesold["quantity"]):
            return JsonResponse({"error": "Insufficient amount."}, status=400)
        else:
            share.quantity -= int(sharesold["quantity"])
            if share.quantity == 0:
                share.delete()
            else:
                share.save()
    else:
        return JsonResponse({"error": "Stock not bought."}, status=400)
    return JsonResponse({"message": "Shares successfully sold."}, status=201)


@login_required
def shares(request, type):
    shares = Share.objects.filter(owner=User.objects.get(username=request.user), type=type.lower()).order_by('-id')
    return JsonResponse([share.serialize() for share in shares], safe=False)


@login_required
def tickers(request):
    tickers = Share.objects.values_list('ticker', flat=True).filter(owner=User.objects.get(username=request.user)).order_by('ticker')
    return JsonResponse([ticker for ticker in tickers], safe=False)


@login_required
@csrf_exempt
def updateprice(request, name):
    data = json.loads(request.body)
    search = Share.objects.filter(owner=request.user, ticker=name)
    if len(search) != 0:
        share = Share.objects.get(owner=request.user, ticker=name)
        share.pricecurrent = data["price"]
        share.save()
    else:
        return JsonResponse({"error": "Stock not bought."}, status=400)
    return JsonResponse({"message": "Price successfully changed."}, status=201)


@login_required
@csrf_exempt
def editnotes(request, name):
    data = json.loads(request.body)
    search = Share.objects.filter(owner=request.user, ticker=name)
    if len(search) != 0:
        share = Share.objects.get(owner=request.user, ticker=name)
        share.notes = data["notes"]
        share.save()
    else:
        return JsonResponse({"error": "Stock not bought."}, status=400)
    return JsonResponse({"message": "Notes successfully changed."}, status=201)


@login_required
def share_view(request, name):
    if request.method == "POST":
        search = Share.objects.filter(owner=request.user, ticker=name.upper())
        if len(search) != 0:
            share = Share.objects.get(owner=request.user, ticker=name.upper())
            share.pricecurrent = request.POST["price-form"]
            share.save()
        else:
            return JsonResponse({"error": "Stock not bought."}, status=400)

        share = Share.objects.get(ticker=name.upper())

        if share.type == "stock":
            type = "Stock"
        elif share.type == "etf":
            type = "ETF"
        else:
            type = "Bond"

        events = Event.objects.filter(share_related=share)

        return render(request, "markethelper/sharepage.html", {
            "share": share,
            "total": share.pricecurrent*share.quantity,
            "dynamics": round((share.pricecurrent/share.pricebought-1)*100, 2),
            "type": type,
            "events": events
        })
    else:    
        share = Share.objects.get(ticker=name.upper())

        if share.type == "stock":
            type = "Stock"
        elif share.type == "etf":
            type = "ETF"
        else:
            type = "Bond"

        events_related = Event.objects.filter(share_related=share)
        if len(events_related) == 0:
            events = []
            events.append("No related events.")
        else:
            events = []
            for event in events_related:
                events.append(event.event_name + ", " + str(event.start_date.date()))
        
        return render(request, "markethelper/sharepage.html", {
            "share": share,
            "total": share.pricecurrent*share.quantity,
            "dynamics": round(share.pricecurrent/share.pricebought-1, 2),
            "type": type,
            "events": events
        })

@login_required
def calendar_view(request):
  
    return render(request, "markethelper/calendarpage.html")


@login_required
def events(request):

    all_events = Event.objects.all()

    event_arr = []

    for i in all_events:
        event_sub_arr = {}
        event_sub_arr['id'] = i.id
        event_sub_arr['title'] = i.event_name
        event_sub_arr['start'] = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        event_sub_arr['end'] = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        event_arr.append(event_sub_arr)

    return JsonResponse(event_arr, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    share = request.GET.get("share", None).upper()
    search = Share.objects.filter(owner=request.user, ticker=share)
    if len(search) != 0:
        event = Event(event_name=str(title), share_related=Share.objects.get(ticker=share), start_date=start, end_date=end)
    else:
        event = Event(event_name=str(title), start_date=start, end_date=end)
    event.save()
    data = {}
    return JsonResponse(data)


def update_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    print(event)
    print(event.start_date)
    print(event.end_date)
    print(start)
    print(end)
    event.start_date = start
    event.end_date = end
    event.event_name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove_event(request):
    print(request.body)
    id = request.GET.get("id", None)
    print(id)
    event = Event.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
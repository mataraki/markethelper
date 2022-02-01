from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("deposit", views.deposit, name="deposit"),
    path("buy", views.buy, name="buy"),
    path("sell", views.sell, name="sell"),
    path("shares/<str:type>", views.shares, name="shares"),
    path("share/<str:name>", views.share_view, name="sharepage"),
    path("share/<str:name>/updateprice", views.updateprice, name="updateprice"),
    path("share/<str:name>/editnotes", views.editnotes, name="editnotes"),
    path("tickers", views.tickers, name="tickers"),
    path("calendar", views.calendar_view, name="calendarpage"),
    path("events", views.events, name="events"),
    path("add_event", views.add_event, name="add_event"),
    path("update_event", views.update_event, name="update_event"),
    path("remove_event", views.remove_event, name="remove_event")
]

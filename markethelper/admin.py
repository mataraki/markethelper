from django.contrib import admin

from .models import User, Share, Event

admin.site.register(User)
admin.site.register(Share)
admin.site.register(Event)

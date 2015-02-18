from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Event
admin.site.register(Event, LeafletGeoAdmin)

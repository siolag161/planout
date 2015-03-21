from django.contrib import admin
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Location

class LocationAdmin(admin.ModelAdmin):
    exclude = ('',)

#admin.site.register(Location,LocationAdmin)
admin.site.register(Location, LeafletGeoAdmin)

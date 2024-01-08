from django.contrib import admin
from .models import *


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # list_display_links = ('id', 'name')

admin.site.register(Car)
admin.site.register(Region)
admin.site.register(Options)
admin.site.register(CarModel)
admin.site.register(Specifications)
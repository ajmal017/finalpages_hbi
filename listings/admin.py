from django.contrib import admin

from .models import Listing

"""
class ListingAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor')
  list_display_links = ('id', 'title')
  list_filter = ('realtor',)
  list_editable = ('is_published',)
  search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
  list_per_page = 25
"""

class ListingAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'contributor', 'type', 'country', 'docfile', 'cover')
  list_display_links = ('title', 'type')
  list_filter = ('type', 'country')
  search_fields = ('title', 'contributor', 'type', 'country')
  list_per_page = 25

admin.site.register(Listing, ListingAdmin)


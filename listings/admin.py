from django.contrib import admin

from .models import Listing, Eproof

class ListingAdmin(admin.ModelAdmin):
  #list_display = ('id', 'title', 'contributor', 'type', 'country', 'docfile', 'cover')
  list_display = ('id', 'title', 'contributor', 'type', 'country', 'is_published')
  list_display_links = ('title', 'type')
  list_filter = ('type', 'country')
  search_fields = ('title', 'contributor', 'type', 'country')
  list_per_page = 25

admin.site.register(Listing, ListingAdmin)
admin.site.register(Eproof)

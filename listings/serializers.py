from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['id', 'title', 'type', 'list_date', 'is_published']
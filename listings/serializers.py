from rest_framework import serializers
from .models import Listing, Product

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['id', 'title', 'type', 'list_date', 'is_published']
		#fields = ['id', 'title', 'type', 'is_published']

class ListingSerializer_COPY(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ['id', 'title', 'type', 'list_date', 'is_published']
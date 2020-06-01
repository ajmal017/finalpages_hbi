from django.forms import ModelForm
from .models import Listing


class ListingForm(ModelForm):
    #title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title123', }))
    #country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled'}))
    #type = forms.ChoiceField(choices=DOCUMENT_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled',}))
    #contributor = forms.CharField(widget=forms.HiddenInput())


    class Meta:
        model = Listing
        fields = '__all__'
        #exclude = ['list_date']
        exclude = ['contributor', 'type', 'list_date']

class EditListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = '__all__'
		#exclude = ['username', 'items_per_page']


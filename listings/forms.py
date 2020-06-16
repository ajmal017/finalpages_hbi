from django.forms import ModelForm
from .models import Listing, Eproof


class ListingForm(ModelForm):
    #title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title123', }))
    #country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled'}))
    #type = forms.ChoiceField(choices=DOCUMENT_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled',}))
    #contributor = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['contributor', 'type', 'list_date']


class EditListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = '__all__'
		exclude = ['contributor', 'type', 'list_date']

class EproofForm(ModelForm):
	class Meta:
		model = Eproof
		fields = '__all__'
		exclude = ['contributor', 'list_date']

from django.forms import ModelForm
from .models import Listing, Eproof, Product
from django import forms


class UploadEproofForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'image2_file', 'image3_file', 'list_date']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'placeholder': 'Type Eproof Title Here'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'image2_file': forms.FileInput(attrs={'class': 'form-control'}),
			'image3_file': forms.FileInput(attrs={'class': 'form-control'}),
			'list_date': forms.HiddenInput()

		}

class UploadBrochureForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'cover_file', 'image1_file', 'image2_file', 'image3_file', 'list_date']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'placeholder': 'Type Brochure Title Here'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'cover_file': forms.FileInput(attrs={'class': 'form-control'}),
			'list_date': forms.HiddenInput()
		}

class EditBrochureForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'document_file', 'cover_file', 'image1_file', 'image2_file', 'image3_file']




########################################################################################################################

class UploadEproofForm_OLD(ModelForm):
	class Meta:
		model = Eproof
		fields = ['eproof_document', 'card_image', 'title', 'description']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'placeholder': 'Type Eproof Title Here'}),
			'card_image': forms.FileInput(attrs={'class': 'form-control'}),
			'eproof_document': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
		}

class UploadDocumentForm(ModelForm):
	class Meta:
		model = Listing
		fields = ['document_file', 'preview_1', 'preview_2', 'preview_3', 'cover', 'title', 'description']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title', 'required': True}),
			'cover': forms.FileInput(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id', 'required': True}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
		}


class EditDocumentForm(ModelForm):
	class Meta:
		model = Listing
		fields = ['document_file', 'preview_1', 'preview_2', 'preview_3', 'cover', 'title', 'description']

		"""
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'eproof_title'}),
			'cover': forms.FileInput(attrs={'class': 'form-control'}),
			'document_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'eproof_document_id'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
		}
		"""

class EditListingForm(ModelForm):
	# title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title123', }))
	# country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled'}))
	# type = forms.ChoiceField(choices=DOCUMENT_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled',}))
	# contributor = forms.CharField(widget=forms.HiddenInput())
	class Meta:
		model = Listing
		fields = '__all__'
		exclude = ['contributor', 'type', 'list_date']

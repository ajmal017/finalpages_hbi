from django import forms
from .models import Listing

from django.conf import settings
User = settings.AUTH_USER_MODEL

class ListingForm(forms.ModelForm):
    #title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'title123', }))
    #country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled'}))
    #type = forms.ChoiceField(choices=DOCUMENT_CHOICES, widget=forms.Select(attrs={'disabled': 'disabled',}))
    #contributor = forms.CharField(widget=forms.HiddenInput())


    class Meta:
        model = Listing
        #fields = ('title', 'description', 'country', 'docfile', 'cover')
        fields = ('title', 'contributor', 'description', 'type', 'country', 'docfile', 'cover' , 'preview_1', 'preview_2', 'preview_3', 'list_date')

"""
    def is_valid(self, form):
        print('123 at function is_valid')
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.contributor = MemberProfile.objects.get(pk=self.kwargs.get('pk'))
        return super(ListingForm, self).form_valid(form)
        #forms.instance.User = self.request.user
        #c = contributor.objects.get(id=1)
        #forms.instance.Company = c
        #return super(group1CreateView, self).form_valid(forms)
"""
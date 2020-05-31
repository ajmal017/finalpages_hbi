from django import forms
from .models import ProposalModel, PurchaseOrderModel, ProductModel

#creates a format and attributes from scratch
class RawProductForm(forms.Form):
    title = forms.CharField(label='My Title', widget=forms.TextInput(attrs={"placeholder": "Enter Title",}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
              "class": "new-class-name two",
              "id": "my-id-for-textarea",
              "rows": 20,
              "cols": 120
            }))
    price = forms.DecimalField(initial = 1.99)

#takes the format and attributes from a Model Class
class ProductForm(forms.ModelForm):
    title = forms.CharField(label='My Title', widget=forms.TextInput(attrs={"placeholder": "Enter Title", }))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "new-class-name two",
                "id": "my-id-for-textarea",
                "rows": 20,
                "cols": 120
            }))
    price = forms.DecimalField(initial=2.99)
    #description = forms.CharField(initial="This is pre-determined description")
    class Meta:
        model = ProductModel
        fields = ('title', 'description', 'price')


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ProposalModel
        fields = ('title', 'author', 'description', 'pdf', 'cover')
        #fields = ('title', 'author', 'pdf', 'cover')


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderModel
        fields = ('title', 'author', 'description', 'pdf', 'cover')

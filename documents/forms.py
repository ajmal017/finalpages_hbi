from django import forms

from .models import Proposal, PurchaseOrder


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('title', 'author', 'description', 'pdf', 'cover')


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ('title', 'author', 'description', 'pdf', 'cover')

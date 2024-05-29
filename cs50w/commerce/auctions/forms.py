from django import forms

from auctions.models import Category


class ListingForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=250, required=True, widget=forms.Textarea())
    starting_bid = forms.FloatField(min_value=0.1, required=True)
    image_url = forms.URLField()
    category = forms.CharField(widget=forms.Select(choices=[(c.pk, c.name) for c in Category.objects.all()]))
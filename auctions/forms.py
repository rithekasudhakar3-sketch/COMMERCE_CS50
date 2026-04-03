from django import forms
from .models import Listing,Comment,WatchList,Bids

class ListingForm(forms.ModelForm):
   class Meta: 
    model = Listing
    fields = "__all__"
class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ["amount"]  # user only needs to enter the amount

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # user only needs to type the comment

class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = []  # no fields needed, just a submit button is enough
class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields =['amount']


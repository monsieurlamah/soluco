from django import forms
from core.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Écrire un commentaire...', 'class':'form-control', 'label':'Votre avis'}))
    
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
from django import forms
from django.forms import ImageField, FileInput, DateInput
from prefinancement.models import ClientTerrain, ClientContruction

class DateInput(forms.DateInput):
    input_type = 'date'
    
class ClientTerrainForm(forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)
    
    class Meta:
        model = ClientTerrain
        fields = ['full_name', 'image', 'marrital_status', 'gender', 'identity_type', 'identity_image', 'date_of_birth', 'signature', 'country', 'state', 'city', 'mobile', 'fax']
        widgets = {
            "full_name":forms.TextInput(attrs={"placeholder":"Prénom et Nom"}),
            "mobile":forms.TextInput(attrs={"placeholder":"Numéro de téléphone"}),
            "fax":forms.TextInput(attrs={"placeholder":"Numéro de fax"}),
            "country":forms.TextInput(attrs={"placeholder":"Pays"}),
            "state":forms.TextInput(attrs={"placeholder":"État"}),
            "city":forms.TextInput(attrs={"placeholder":"Ville"}),
            "date_of_birth":DateInput
        }
        

class ClientContructionForm(forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)
    documents = ImageField(widget=FileInput)
    
    class Meta:
        model = ClientContruction
        fields = ['full_name', 'image', 'marrital_status', 'gender', 'identity_type', 'identity_image', 'date_of_birth', 'signature','documents', 'country', 'state', 'city', 'mobile', 'fax']
        widgets = {
            "full_name":forms.TextInput(attrs={"placeholder":"Prénom et Nom"}),
            "mobile":forms.TextInput(attrs={"placeholder":"Numéro de téléphone"}),
            "fax":forms.TextInput(attrs={"placeholder":"Numéro de fax"}),
            "country":forms.TextInput(attrs={"placeholder":"Pays"}),
            "state":forms.TextInput(attrs={"placeholder":"État"}),
            "city":forms.TextInput(attrs={"placeholder":"Ville"}),
            "date_of_birth":DateInput
        }
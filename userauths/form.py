from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'maxlength':10}),
                             error_messages={'required': 'Veuillez entrer un nom d\'utilisateur.'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'E-mail'}),
                           error_messages={'required': 'Veuillez entrer une adresse e-mail valide.'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
                              error_messages={'required': 'Veuillez entrer un mot de passe.'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmation du mot de passe'}),
                              error_messages={'required': 'Veuillez entrer une confirmation du mot de passe.'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
        
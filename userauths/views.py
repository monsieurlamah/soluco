from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from userauths.form import UserRegisterForm
from userauths.models import User

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Vous êtes déjà connecté')
        return redirect('core-index')
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Salut {username}, votre compte a été créé.")
            new_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core-index")            
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous êtes connecté avec succès !')
                return redirect("core-index")
            else:
                messages.warning(request, "L'email ou le mot de passe est incorrect")
                return redirect("userauths-sign-in")
        except:
            messages.warning(request, f"L'utilisateur avec {email} n'existe pas")
    
    if request.user.is_authenticated:
        messages.warning(request, "Vous êtes déjà connecté")
        return redirect("core-index")
    return render(request, 'userauths/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté")
    return redirect("core-index")
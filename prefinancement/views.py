from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from prefinancement.models import ClientTerrain, ClientContruction, Account
from prefinancement.forms import ClientTerrainForm, ClientContructionForm
from django.contrib import messages

@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            client_terrain = ClientTerrain.get(user=request.user)
            client_contruction = ClientContruction.get(user=request.user)
        except:
            messages.warning(request, "Vous devez soummettre votre formulaire")
            return redirect("core-dashboard")
        
        account = Account.objects.get(user=request.user)
        
    else:
        messages.warning(request, "Vous devez être connecté pour accéder à votre compte")
        return redirect("userauths-sign-in")
    
    context = {
        'client_terrain':client_terrain,
        'client_contruction':client_contruction,
        'account':account
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def clientTerrain_register(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    try:
        client_terrain = ClientTerrain.objects.get(user=user)
    except:
        client_terrain = None
    
    if request.method == "POST":
        form_terrain = ClientTerrainForm(request.POST, request.FILES, instance=client_terrain)
        if form_terrain.is_valid():
            new_form = form_terrain.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "Votre formulaire est soumis avec succès, en cours de révision pour le préfinancement.")
            return redirect("core-index")
    else:
        form_terrain = ClientTerrainForm()
    context = {
        'account':account,
        'form_terrain':form_terrain, 
        'client_terrain':client_terrain
    }
    return render(request, 'prefinancement/client-terrain.html', context)
            

@login_required
def clientContruction_register(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    try:
        client_contruction = ClientContruction.objects.get(user=user)
    except:
        client_contruction = None
        
    if request.method == "POST":
        form = ClientContructionForm(request.POST, request.FILES, instance=client_contruction)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "Votre formulaire est soumis avec succès, en cours de révision pour le préfinancement.")
            return redirect("core-index")
    else:
        form = ClientContructionForm()
    context = {
        'account':account,
        'form':form, 
        'client_contruction':client_contruction
    }
    return render(request, 'prefinancement/client-contruction.html', context)
      
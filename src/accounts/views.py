from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

#Connexion
def login_user(request):
    if request.method =="POST":
        #connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")

    #vérifier que l'utilisateur est bien dans la base de donnée
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
            
    return render(request, 'accounts/login.html')

#Déconnexion
def logout_user(request):
    logout(request)
    return redirect('home')
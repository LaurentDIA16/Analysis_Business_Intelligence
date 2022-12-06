from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

#Connexion
# def login_user(request):
#     if request.method =="POST":
#         #connecter l'utilisateur
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#     #vérifier que l'utilisateur est bien dans la base de donnée
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('home')
            
#     return render(request, 'accounts/login.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')     

        else:
            messages.success(request, 'Erreur, veuillez réessayez ...')
            return redirect('login')     
    
    else:
        return render(request, 'accounts/login.html', {})

#Déconnexion
# def logout_user(request):
#     logout(request)
#     return redirect('login')

def logout_user(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté!!!")
    return redirect('login')
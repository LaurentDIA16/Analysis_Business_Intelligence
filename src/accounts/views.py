from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomAddUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields

def add_user(request):
    context = {}

    if request.method == "POST":
        form = CustomAddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nouvel utilisateur créé")
            return redirect('home')
        else:
            context["errors"] = form.errors
    
    form = CustomAddUserForm()
    context["form"] = form

    return render(request, "accounts/add-user.html", context={"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')     

        else:
            messages.error(request, 'Erreur, veuillez réessayez ...')
            return redirect('login')     
    
    else:
        return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request, "Vous êtes déconnecté!!!")
    return redirect('login')


# if request.method == "POST":
#         username = request.POST.get("username")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         if password1 != password2:
#             return render(request, "accounts/register.html", {"error": "Les mots de passes ne correspondent pas!!!"})
#         CustomUser.objects.create_user(username=username, password=password1)
#         messages.success(request, "L'utilisateur à été créé")
#         return redirect('home')
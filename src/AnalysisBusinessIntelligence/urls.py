"""AnalysisBusinessIntelligence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard.views import home, import_csv, cleanData, sellByCountryTop, sellByCountryFlop, sellByProductTop
from accounts.views import login_user, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("import/", import_csv, name="import"),
    path("import/nettoyer/", cleanData, name="nettoyer"), 
    path("connexion/", login_user, name="login"),
    path("déconnexion/", logout_user, name="logout"),
    path("graphique-region/", sellByCountryTop, name="graphique-region"),
    path("graphique-region/Flop", sellByCountryFlop, name="graphique-region-flop"),
    path("graphique-produit/", sellByProductTop, name="graphique-produit"),
    path("graphique-produit/Flop", sellByProductTop, name="graphique-produit"),   
]




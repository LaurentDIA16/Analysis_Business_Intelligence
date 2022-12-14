from django.contrib import admin
from django.urls import path
from dashboard.views import home, import_csv, analyseData, cleanData, deleteData
from dashboard.views import sellByCountryTop, sellByCountryFlop, sellByProductTop, sellByProductFlop, sellByCountryProduct 
from accounts.views import login_user, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("import/", import_csv, name="import"),
    path("import/analyser/", analyseData, name="analyser"),
    path("import/nettoyer/", cleanData, name="nettoyer"),
    path("supprimer-données/", deleteData, name="supprimer-données"),
    path("connexion/", login_user, name="login"),
    path("déconnexion/", logout_user, name="logout"),
    path("graphique-region/", sellByCountryTop, name="graphique-region"),
    path("graphique-region/Flop", sellByCountryFlop, name="graphique-region-flop"),
    path("graphique-produit/", sellByProductTop, name="graphique-produit"),
    path("graphique-produit/Flop", sellByProductFlop, name="graphique-produit-flop"),
    path("graphique-region-produit/", sellByCountryProduct, name="graphique-region-produit"),   
]




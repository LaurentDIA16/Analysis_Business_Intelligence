from django.contrib import admin
from django.urls import path
from dashboard.views import home, import_csv, analyseData, cleanData, deleteData
from dashboard.views import sellByCountryTop, sellByCountryTop2010, sellByCountryTop2011, sellByCountryFlop, sellByCountryFlop2010, sellByCountryFlop2011
from dashboard.views import sellByProductTop, sellByProductTop2010, sellByProductTop2011, sellByProductFlop, sellByProductFlop2010, sellByProductFlop2011
from dashboard.views import sellByCountryProduct, sellByMonth
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
    path("graphique-region/top/", sellByCountryTop, name="graphique-region-top"),
    path("graphique-region/top/2010/", sellByCountryTop2010, name="graphique-region-top-2010"),
    path("graphique-region/top/2011/", sellByCountryTop2011, name="graphique-region-top-2011"),
    path("graphique-region/flop/", sellByCountryFlop, name="graphique-region-flop"),
    path("graphique-region/flop/2010/", sellByCountryFlop2010, name="graphique-region-flop-2010"),
    path("graphique-region/flop/2011/", sellByCountryFlop2011, name="graphique-region-flop-2011"),
    path("graphique-region/flop/", sellByCountryFlop, name="graphique-region-flop"),
    path("graphique-produit/top/", sellByProductTop, name="graphique-produit-top"),
    path("graphique-produit/", sellByProductTop, name="graphique-produit"),
    path("graphique-produit/top/2010/", sellByProductTop2010, name="graphique-produit-top-2010"),
    path("graphique-produit/top/2011/", sellByProductTop2011, name="graphique-produit-top-2011"),
    path("graphique-produit/flop/", sellByProductFlop, name="graphique-produit-flop"),
    path("graphique-produit/flop/2010/", sellByProductFlop2010, name="graphique-produit-flop-2010"),
    path("graphique-produit/flop/2011/", sellByProductFlop2011, name="graphique-produit-flop-2011"),
    path("graphique-region-produit/", sellByCountryProduct, name="graphique-region-produit"),   
    path("graphique-vente-mensuelle/", sellByMonth, name="graphique-vente-mensuelle"),
]




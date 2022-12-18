from django.contrib import admin
from django.urls import path
from dashboard.views import home, import_csv, analyseData, cleanData, deleteData
from dashboard.views import sellByCountryTop, sellByCountryTop2010, sellByCountryTop2011, sellByCountryFlop, sellByCountryFlop2010, sellByCountryFlop2011
from dashboard.views import sellByProductTop, sellByProductTop2010, sellByProductTop2011, sellByProductFlop, sellByProductFlop2010, sellByProductFlop2011
from dashboard.views import sellByCountryProductTop, sellByCountryProductTop2010, sellByCountryProductTop2011, sellByCountryProductFlop, sellByCountryProductFlop2010, sellByCountryProductFlop2011 
from dashboard.views import sellByCountryProductOne, sellByMonth, listProduct
from accounts.views import add_user, login_user, logout_user

urlpatterns = [
    path('AnalysisBusinessIntelligence/admin/', admin.site.urls),
    path("AnalysisBusinessIntelligence/compte/ajouter/", add_user, name="add-user"),    
    path("AnalysisBusinessIntelligence/compte/connexion/", login_user, name="login"),
    path("AnalysisBusinessIntelligence/compte/déconnexion/", logout_user, name="logout"),
    path("AnalysisBusinessIntelligence/Dashboard/", home, name="home"),
    path("AnalysisBusinessIntelligence/import/", import_csv, name="import"),
    path("AnalysisBusinessIntelligence/import/analyser/", analyseData, name="analyser"),
    path("AnalysisBusinessIntelligence/import/nettoyer/", cleanData, name="nettoyer"),
    path("AnalysisBusinessIntelligence/supprimer-données/", deleteData, name="supprimer-données"),
    path("AnalysisBusinessIntelligence/graphique-region/", sellByCountryTop, name="graphique-region"),
    path("AnalysisBusinessIntelligence/graphique-region/top/", sellByCountryTop, name="graphique-region-top"),
    path("AnalysisBusinessIntelligence/graphique-region/top/2010/", sellByCountryTop2010, name="graphique-region-top-2010"),
    path("AnalysisBusinessIntelligence/graphique-region/top/2011/", sellByCountryTop2011, name="graphique-region-top-2011"),
    path("AnalysisBusinessIntelligence/graphique-region/flop/", sellByCountryFlop, name="graphique-region-flop"),
    path("AnalysisBusinessIntelligence/graphique-region/flop/2010/", sellByCountryFlop2010, name="graphique-region-flop-2010"),
    path("AnalysisBusinessIntelligence/graphique-region/flop/2011/", sellByCountryFlop2011, name="graphique-region-flop-2011"),
    path("AnalysisBusinessIntelligence/graphique-region/flop/", sellByCountryFlop, name="graphique-region-flop"),
    path("AnalysisBusinessIntelligence/graphique-produit/top/", sellByProductTop, name="graphique-produit-top"),
    path("AnalysisBusinessIntelligence/graphique-produit/", sellByProductTop, name="graphique-produit"),
    path("AnalysisBusinessIntelligence/graphique-produit/top/2010/", sellByProductTop2010, name="graphique-produit-top-2010"),
    path("AnalysisBusinessIntelligence/graphique-produit/top/2011/", sellByProductTop2011, name="graphique-produit-top-2011"),
    path("AnalysisBusinessIntelligence/graphique-produit/flop/", sellByProductFlop, name="graphique-produit-flop"),
    path("AnalysisBusinessIntelligence/graphique-produit/flop/2010/", sellByProductFlop2010, name="graphique-produit-flop-2010"),
    path("AnalysisBusinessIntelligence/graphique-produit/flop/2011/", sellByProductFlop2011, name="graphique-produit-flop-2011"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/", sellByCountryProductTop, name="graphique-region-produit"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/top/", sellByCountryProductTop, name="graphique-region-produit-top"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/top/2010/", sellByCountryProductTop2010, name="graphique-region-produit-top-2010"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/top/2011/", sellByCountryProductTop2011, name="graphique-region-produit-top-2011"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/flop/", sellByCountryProductFlop, name="graphique-region-produit-flop"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/flop/2010/", sellByCountryProductFlop2010, name="graphique-region-produit-flop-2010"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/flop/2011/", sellByCountryProductFlop2011, name="graphique-region-produit-flop-2011"),
    path("AnalysisBusinessIntelligence/graphique-vente-mensuelle/", sellByMonth, name="graphique-vente-mensuelle"),
    path("AnalysisBusinessIntelligence/graphique-region-produit/UK", sellByCountryProductOne, name="graphique-region-produit-uk"),
    path("AnalysisBusinessIntelligence/liste-produit/", listProduct, name="liste-produit"),
]




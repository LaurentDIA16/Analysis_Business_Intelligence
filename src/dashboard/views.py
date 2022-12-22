from multiprocessing import connection
from django.shortcuts import render, redirect
from dashboard.forms import InputFileForm
from dashboard.functions.functions import handle_uploaded_file
from .models import *
from django.conf import settings
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from django.contrib import messages
import psycopg2
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    
    invoices = Invoice.objects.all().count()
    products = Product.objects.all().count()
    countries = Country.objects.all().count()
    earningsfloat = DetailInvoice.objects.annotate(as_float=Cast('totalcost', FloatField())).aggregate(Sum('as_float'))
    try:
        # earningsfloat.int(earningsfloat['as_float__sum'])
        earningsfloat = int(earningsfloat['as_float__sum'])
    except:
        pass
    
    context = {'invoices':invoices,'products':products,'countries':countries, 'earningsfloat':earningsfloat}

    return render(request,"dashboard/home.html", context)

@login_required(login_url='login')
def import_csv(request):
    #Pour garder le filtrage du Dropdown Graphique si pas de data
    invoices = Invoice.objects.all().count()

    #Importer CSV
    if request.method == 'POST':  
        csvFile = InputFileForm(request.POST, request.FILES)  
        if csvFile.is_valid():  
            handle_uploaded_file(request.FILES['file'])
            analyseData(request)
            messages.success(request, 'CSV importé avec succès!')
            return redirect('analyser')
    
    else:  
        csvFile = InputFileForm()

        #Supprimer un fichier CSV si présent
        for folder, subfolders, files in os.walk('dashboard/static/upload'): 
            for file in files: 
                # Vérifier si le fichir fini en .csv 
                if file.endswith('.csv'): 
                    path = os.path.join(folder, file)      
                    print('deleted : ', path )
                    # supprimer le csv 
                    os.remove(path)

        return render(request,"dashboard/import.html",{'form':csvFile, 'invoices':invoices})
    
@login_required(login_url='login')
def analyseData(request):
        
        #Création variable stockage data
        dataset_dir = 'dashboard/static/upload'

        #Création du chemin du fichier CSV
        csv_file = os.getcwd()+'/'+dataset_dir+'/'+"data.csv"

        #Création du dataframe depuis le fichier CSV
        df = pd.read_csv(csv_file, encoding= 'unicode_escape')

        #Mettre en minuscule les noms de colonnes
        df.columns = [x.lower() for x in df.columns]

        ######################## Comptabiliser les données à supprimer #########################
        #Comptabiliser le nombre de lignes de ventes originales
        nbOriginalData = df.index.size
        nbOriginalData = int(nbOriginalData)

        #Comptabiliser les lignes doublons
        nbDuplicated = df.duplicated().sum()
        nbDuplicated = int(nbDuplicated)

        #Comptabiliser les doublons invoice/stockcode
        nbDuplicatedCol = df.duplicated(['invoiceno','stockcode']).sum()
        nbDuplicatedCol = int(nbDuplicatedCol)

        #Comptabiliser les lignes quantity <=0
        indexQuantity = df[df['quantity']<=0].index.size
        nbQuantity0 = int(indexQuantity)

        # Comptabiliser les lignes unitprice <= 0
        indexUnitPrice = df[df['unitprice']<=0].index.size
        nbUnitPrice0 = int(indexUnitPrice)

        # Comptabiliser les lignes stockcode qui commence par une chaîne de caractère
        indexStockCode = df[df["stockcode"].str.match("^[A-Za-z]")==True].index.size
        nbStartChar = int(indexStockCode)

        #### Total données à supprimer ####
        dataToDelete = nbDuplicated + nbQuantity0 + nbUnitPrice0 + nbStartChar
        
        ##################### Comptabiliser les données à réparer #############################
        #Mettre en minuscule le nom des pays
        lowerCase = df['country'].size
        lowerCase = int(lowerCase)

        #Tous les champs vide dans la DataFrame (colonne CustomerID, colonne Description)
        nbNull = df.isnull().sum().sum()
        nbNull = int(nbNull)

        #### Total données à réparer ####
        dataToRepair = lowerCase + nbNull

        ##################### Récapitulatif de l'analyse ##########################
        dataOrigin = f"Nombre de lignes de ventes: {nbOriginalData}"
        dataToDelete = f"Nombre de lignes à supprimer: {dataToDelete}"
        dataToRepair = f"Nombre de champs réparable: {dataToRepair}"

        ################## Après nettoyage ######################
        
        #Total données restantes
        dataFinal = nbOriginalData - (nbDuplicated + nbQuantity0 + nbUnitPrice0 + nbStartChar)

        #Pourcentage de donnée à supprimer
        percDataDelete = ((nbDuplicated + nbQuantity0 + nbUnitPrice0 + nbStartChar)/nbOriginalData)*100
        percDataDeleteFloat = round(percDataDelete,2)

        ################ Récapitulatif si donnée supprimer ################@
        dataFinal = f"Nombre de lignes de ventes: {dataFinal}"
        percDataDelete = f"Pourcentage suppression: {round(percDataDelete,2)} %"

        #Pour garder le filtrage du Dropdown Graphique Navbar pour ne pas qu'il s'affiche
        invoices = Invoice.objects.all().count()

        context = {'dataOrigin':dataOrigin, 
                   'dataToDelete':dataToDelete, 
                   'dataToRepair':dataToRepair,
                   'dataFinal':dataFinal,
                   'percDataDelete':percDataDelete,
                   'percDataDeleteFloat':percDataDeleteFloat,
                   'invoices':invoices}

        return render(request, 'dashboard/import-analyser.html', context )

@login_required(login_url='login')
def cleanData(self, *args, **options):

    try:
        #Création variable stockage data
        dataset_dir = 'dashboard/static/upload'

        # #Création du chemin du fichier CSV
        csv_file = os.getcwd()+'/'+dataset_dir+'/'+"data.csv"

        # #Création du dataframe depuis le fichier CSV
        df = pd.read_csv(csv_file, encoding= 'unicode_escape')
        # nbOriginalData = df.shape[0]

        # #Mettre en minuscule les noms de colonnes
        df.columns = [x.lower() for x in df.columns]

        #Ajouter une colonne totalcost pour calculer le prix * quantité
        df['totalcost'] = df.unitprice * df.quantity
        
        #Supprimer les lignes doublon
        df = df.drop_duplicates()
        
        # nbDuplicated = df.duplicated().sum()

        #Supprimer les doublons invoice/stockcode
        df = df.drop_duplicates(['invoiceno','stockcode'])

        # nbDuplicatedCol = df.duplicated(['invoiceno','stockcode']).sum()

        #Supprimer les lignes quantity <=0
        indexQuantity = df[df['quantity']<=0].index
        df.drop(indexQuantity,inplace=True)

         # nbQuantity0 = indexQuantity.value_counts()

        #Supprimer les lignes unitprice = 0
        indexUnitPrice = df[df['unitprice']<=0].index
        df.drop(indexUnitPrice,inplace=True)

        # nbUnitPrice0 = indexUnitPrice.value_counts()

        #Supprimer les lignes stockcode qui commence par une chaîne de caractère
        indexStockCode = df[df["stockcode"].str.match("^[A-Za-z]")==True].index
        df.drop(indexStockCode,inplace=True)

        # nbStartChar = indexStockCode.value_counts()
        # nbFinalData = df.shape[0]

        # Mettre en Minuscule les lignes country EIRE -> Eire
        df['country'] = df['country'].str.title()

        #Mettre les lignes avec country NULL ou Numérique en "unspecified"
        df.replace('NaN',np.nan)
        df['country'].fillna(value='Unspecified')
        df['description'].fillna(value='Description du produit à intégrer')

        #si les autres colonnes ont un intérêt
        # nbCountryNan = df['country'].isnull().sum()

        #Afficher le % de suppression et si <5% dire "envisageable"
        # nbDeleteData = nbOriginalData - nbFinalData
        # percFinalData = 100-((nbDeleteData*100)/nbOriginalData)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user,password=password,database_name=database_name)
        engine = create_engine(database_url, echo=False)

        #Transfert de la Dataframe dans une table temporaire de la BDD
        df.to_sql(Datatransfert._meta.db_table, if_exists='replace', con=engine, index=False)
        
        #Requête pour envoi data dans les différentes tables de la BDD
        sql = '''

        ALTER TABLE dashboard_invoice
            ALTER COLUMN invoicedate TYPE text;

        SET CONSTRAINTS ALL IMMEDIATE;

        INSERT INTO dashboard_country(country)
            SELECT country
            FROM dashboard_datatransfert
            ON CONFLICT(country)
            DO NOTHING;

        INSERT INTO dashboard_product(stockcode,description)
            SELECT stockcode,description
            FROM dashboard_datatransfert
            ON CONFLICT(stockcode)
            DO NOTHING;
        
        INSERT INTO dashboard_invoice(invoiceno,invoicedate,customerid,country)
            SELECT invoiceno,invoicedate,customerid,country
            FROM dashboard_datatransfert
            ON CONFLICT(invoiceno)
            DO NOTHING;

        INSERT INTO dashboard_detailinvoice(invoiceno,stockcode,unitprice,quantity,totalcost)
            SELECT invoiceno,stockcode,unitprice,quantity,totalcost
            FROM dashboard_datatransfert
            ON CONFLICT
            DO NOTHING;

        UPDATE dashboard_country SET zone='Earth';

        DELETE FROM dashboard_datatransfert;

        ALTER TABLE dashboard_invoice
            ALTER COLUMN invoicedate TYPE date
            USING invoicedate::date;

        '''

        #Executer la requête pour envoi dans la BDD Postgre
        engine.execute(sql)

        #Supprimer le fichier CSV importé
        for folder, subfolders, files in os.walk('dashboard/static/upload'): 
            for file in files: 
                # Vérifier si le fichir fini en .csv 
                if file.endswith('.csv'): 
                    path = os.path.join(folder, file)      
                    print('deleted : ', path )
                    # supprimer le csv 
                    os.remove(path)
    except FileNotFoundError as e:
        print("Veuillez importer un fichier CSV d'abord")
    
    messages.success(self, 'CSV nettoyé et enregistré dans la base de donnée!')
    return redirect("import")

@login_required(login_url='login')
def deleteData(self):

    detailInvoices = DetailInvoice.objects.all().delete()
    invoices = Invoice.objects.all().delete()
    products = Product.objects.all().delete()
    countries = Country.objects.all().delete()

    # context = {'invoices':invoices, 'detailInvoices':detailInvoices, 'products':products, 'countries':countries}
    messages.success(self, "Les données ont été supprimés de la base de données")
    return redirect('home')

@login_required(login_url='login')
def sellByCountryTop(request):

    sql = '''SELECT dashboard_invoice.country, count(*) 
                FROM dashboard_detailinvoice 
                INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                GROUP BY dashboard_invoice.country
                ORDER BY count DESC 
                LIMIT 10'''

    res = Country.objects.raw(sql)
    top = 'all years'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-region.html", context)

@login_required(login_url='login')
def sellByCountryTop2010(request):
    
    sql = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                FROM dashboard_invoice as i
                INNER JOIN dashboard_detailinvoice as di
                ON i.invoiceno = di.invoiceno
                WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                ORDER BY count DESC
                LIMIT 10'''
    
    res = Country.objects.raw(sql)
    top = '2010'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-region.html", context)

@login_required(login_url='login')
def sellByCountryTop2011(request):
    
    sql = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                FROM dashboard_invoice as i
                INNER JOIN dashboard_detailinvoice as di
                ON i.invoiceno = di.invoiceno
                WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                ORDER BY count DESC
                LIMIT 10'''
    
    res = Country.objects.raw(sql)
    top = '2011'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-region.html", context)

@login_required(login_url='login')
def sellByCountryFlop(request):

    sql = '''SELECT dashboard_invoice.country, count(*) 
                FROM dashboard_detailinvoice 
                INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                GROUP BY dashboard_invoice.country
                ORDER BY count ASC 
                LIMIT 10'''

    res = Country.objects.raw(sql)

    return render(request, "dashboard/graphique-region.html", {'data': res})

@login_required(login_url='login')
def sellByCountryFlop2010(request):
    
    sql = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                FROM dashboard_invoice as i
                INNER JOIN dashboard_detailinvoice as di
                ON i.invoiceno = di.invoiceno
                WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                ORDER BY count ASC
                LIMIT 10'''
    
    res = Country.objects.raw(sql)

    return render(request, "dashboard/graphique-region.html", {'data': res})

@login_required(login_url='login')
def sellByCountryFlop2011(request):

    sql = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                FROM dashboard_invoice as i
                INNER JOIN dashboard_detailinvoice as di
                ON i.invoiceno = di.invoiceno
                WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                ORDER BY count ASC
                LIMIT 10'''
    
    res = Country.objects.raw(sql)

    return render(request, "dashboard/graphique-region.html", {'data': res})

@login_required(login_url='login')
def sellByProductTop(request):

    sql=('''SELECT dashboard_detailinvoice.stockcode, count(*) 
                FROM dashboard_detailinvoice 
                INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                GROUP BY dashboard_detailinvoice.stockcode
                ORDER BY count DESC 
                LIMIT 10''')

    res = Product.objects.raw(sql)
    top = 'all years'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-produit.html", context)

@login_required(login_url='login')
def sellByProductTop2010(request):

    sql=('''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
			FROM dashboard_invoice as i
			INNER JOIN dashboard_detailinvoice as di
			ON i.invoiceno = di.invoiceno
			WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
			GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
			ORDER BY count DESC
			LIMIT 10''')

    res = Product.objects.raw(sql)
    top = '2010'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-produit.html", context)

@login_required(login_url='login')
def sellByProductTop2011(request):

    sql=('''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
			FROM dashboard_invoice as i
			INNER JOIN dashboard_detailinvoice as di
			ON i.invoiceno = di.invoiceno
			WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
			GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
			ORDER BY count DESC
			LIMIT 10''')

    res = Product.objects.raw(sql)
    top = '2011'

    context = {'data': res, 'top':top}

    return render(request, "dashboard/graphique-produit.html", context)

@login_required(login_url='login')
def sellByProductFlop(request):

    sql=('''SELECT dashboard_detailinvoice.stockcode, count(*) 
                FROM dashboard_detailinvoice 
                INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                GROUP BY dashboard_detailinvoice.stockcode
                ORDER BY count ASC 
                LIMIT 10''')

    res = Product.objects.raw(sql)

    return render(request, "dashboard/graphique-produit.html", {'data': res})

@login_required(login_url='login')
def sellByProductFlop2010(request):

    sql=('''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
			FROM dashboard_invoice as i
			INNER JOIN dashboard_detailinvoice as di
			ON i.invoiceno = di.invoiceno
			WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
			GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
			ORDER BY count ASC
			LIMIT 10''')

    res = Product.objects.raw(sql)

    return render(request, "dashboard/graphique-produit.html", {'data': res})

@login_required(login_url='login')
def sellByProductFlop2011(request):

    sql=('''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
			FROM dashboard_invoice as i
			INNER JOIN dashboard_detailinvoice as di
			ON i.invoiceno = di.invoiceno
			WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
			GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
			ORDER BY count ASC
			LIMIT 10''')

    res = Product.objects.raw(sql)

    return render(request, "dashboard/graphique-produit.html", {'data': res})

@login_required(login_url='login')
def sellByCountryProductTop(request):

    sqlCountry = '''SELECT dashboard_invoice.country, count(*) 
                        FROM dashboard_detailinvoice 
                        INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                        GROUP BY dashboard_invoice.country
                        ORDER BY count DESC 
                        LIMIT 10'''

    
    sqlProduct ='''SELECT dashboard_detailinvoice.stockcode, count(*) 
                        FROM dashboard_detailinvoice 
                        INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                        GROUP BY dashboard_detailinvoice.stockcode
                        ORDER BY count DESC 
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)
    top = 'all years'

    context = {'dataCountry': resCountry,'dataProduct':resProduct, 'top':top}

    return render(request, "dashboard/graphique-region-produit copy.html", context)

@login_required(login_url='login')
def sellByCountryProductTop2010(request):

    sqlCountry = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                        ORDER BY count DESC
                        LIMIT 10'''

    
    sqlProduct ='''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
                        ORDER BY count DESC
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)

    top = '2010'

    context = {'dataCountry': resCountry,'dataProduct':resProduct, 'top':top}

    return render(request, "dashboard/graphique-region-produit.html", context)

@login_required(login_url='login')
def sellByCountryProductTop2011(request):

    sqlCountry = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                        ORDER BY count DESC
                        LIMIT 10'''

    
    sqlProduct ='''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
                        ORDER BY count DESC
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)

    top = '2011'

    context = {'dataCountry': resCountry,'dataProduct':resProduct, 'top':top}

    return render(request, "dashboard/graphique-region-produit.html", context)

@login_required(login_url='login')
def sellByCountryProductFlop(request):
    
    sqlCountry = '''SELECT dashboard_invoice.country, count(*) 
                        FROM dashboard_detailinvoice 
                        INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                        GROUP BY dashboard_invoice.country
                        ORDER BY count ASC 
                        LIMIT 10'''

    
    sqlProduct ='''SELECT dashboard_detailinvoice.stockcode, count(*) 
                        FROM dashboard_detailinvoice 
                        INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                        GROUP BY dashboard_detailinvoice.stockcode
                        ORDER BY count ASC 
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)

    context = {'dataCountry': resCountry,'dataProduct':resProduct}

    return render(request, "dashboard/graphique-region-produit.html", context)

@login_required(login_url='login')
def sellByCountryProductFlop2010(request):

    sqlCountry = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                        ORDER BY count ASC
                        LIMIT 10'''

    
    sqlProduct ='''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2010
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
                        ORDER BY count ASC
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)

    context = {'dataCountry': resCountry,'dataProduct':resProduct}

    return render(request, "dashboard/graphique-region-produit.html", context)

@login_required(login_url='login')
def sellByCountryProductFlop2011(request):

    sqlCountry = '''SELECT EXTRACT(YEAR FROM i.invoicedate), i.country, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), i.country
                        ORDER BY count ASC
                        LIMIT 10'''

    
    sqlProduct ='''SELECT EXTRACT(YEAR FROM i.invoicedate), di.stockcode, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE EXTRACT(YEAR FROM i.invoicedate) = 2011
                        GROUP BY EXTRACT(YEAR FROM i.invoicedate), di.stockcode
                        ORDER BY count ASC
                        LIMIT 10'''
    
    resCountry = Country.objects.raw(sqlCountry)
    resProduct = Product.objects.raw(sqlProduct)

    context = {'dataCountry': resCountry,'dataProduct':resProduct}

    return render(request, "dashboard/graphique-region-produit.html", context)

#va de paire avec la fonction sellBYMonth pour pouvoir mettre les données dans un dictionnaire
def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

@login_required(login_url='login')
def sellByMonth(request):

    #establishing the connection
    conn = psycopg2.connect(
        database="DB_Analysis_Business_Intelligence", user='moni', password='moni', host='127.0.0.1', port= '5432'
    )

    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    cursor.execute('''SELECT EXTRACT(MONTH FROM i.invoicedate) as month, count(*) 
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        GROUP BY EXTRACT(MONTH FROM i.invoicedate)
                        ORDER BY month asc''')

    r = dictfetchall(cursor)

    cursor.execute('''SELECT EXTRACT(MONTH FROM i.invoicedate) as month, ROUND(sum(di.totalcost)) as cout
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        GROUP BY EXTRACT(MONTH FROM i.invoicedate)
                        ORDER BY month asc''')

    r2 = dictfetchall(cursor)

    cursor.close()

    context = {'data1': r, 'data2': r2}

    return render(request, "dashboard/graphique-vente-mensuelle.html", context)

@login_required(login_url='login')
def sellByCountryProductOne(request):

    #establishing the connection
    conn = psycopg2.connect(
        database="DB_Analysis_Business_Intelligence", user='moni', password='moni', host='127.0.0.1', port= '5432'
    )

    #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    cursor.execute('''SELECT di.stockcode, count(di.stockcode), ROUND(sum(di.totalcost)) as cout
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE i.country = 'United Kingdom'
                        GROUP BY di.stockcode
                        ORDER BY cout DESC
                        LIMIT 10''')

    r = dictfetchall(cursor)

    cursor.execute('''SELECT di.stockcode, count(di.stockcode), ROUND(sum(di.totalcost)) as cout
                        FROM dashboard_invoice as i
                        INNER JOIN dashboard_detailinvoice as di
                        ON i.invoiceno = di.invoiceno
                        WHERE i.country = 'United Kingdom'
                        GROUP BY di.stockcode
                        ORDER BY cout DESC
                        LIMIT 10''')

    r2 = dictfetchall(cursor)

    cursor.close()

    context = {'data1': r, 'data2': r2}

    return render(request, "dashboard/graphique-region-produit-uk.html", context)

@login_required(login_url='login')
def listProduct(request):

    sql = '''SELECT pr.stockcode, pr.description, ROUND(AVG(di.unitprice),2) as meanprice
                FROM dashboard_product as pr
                INNER JOIN dashboard_detailinvoice as di
                ON pr.stockcode = di.stockcode
                GROUP BY pr.stockcode, pr.description
                ORDER BY pr.stockcode ASC'''
    
    res = Product.objects.raw(sql)

    context = {'data':res}

    return render(request, "dashboard/liste-produit.html", context)
    

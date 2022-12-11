from django.core.management.base import BaseCommand
import os
import pandas as pd
import numpy as np
from dashboard.models import *
from sqlalchemy import create_engine
from django.conf import settings

class Command(BaseCommand):
    help = 'A command to add data from an CSV file to the database'

    def handle(self, *args, **options):

        #Création variable stockage data
        dataset_dir = 'dashboard/static/upload'

        #Création du chemin du fichier CSV
        csv_file = os.getcwd()+'/'+dataset_dir+'/'+"data.csv"

        #Création du dataframe depuis le fichier CSV
        df = pd.read_csv(csv_file, encoding= 'unicode_escape')
        nbOriginalData = df.shape[0]
        print("Nb de lignes de données originel: " + str(nbOriginalData))

        #Mettre en minuscule les noms de colonnes
        df.columns = [x.lower() for x in df.columns]

        #Ajouter une colonne totalcost pour calculer le prix * quantité
        df['totalcost'] = df.unitprice * df.quantity
        # print(df.head())
        
        #Supprimer les lignes doublons
        nbDuplicated = df.duplicated().sum()
        df = df.drop_duplicates()
        print("Nb de lignes de données doublons: " + str(nbDuplicated))

        #Supprimer les doublons invoice/stockcode
        # print(df.duplicated(['invoiceno','stockcode']).sum())
        nbDuplicatedCol = df.duplicated(['invoiceno','stockcode']).sum()
        df = df.drop_duplicates(['invoiceno','stockcode'])
        print("Nb de lignes de données doublons invoice/stockcode: " + str(nbDuplicatedCol))

        #Supprimer les lignes quantity <=0
        indexQuantity = df[df['quantity']<0].index
        nbQuantity0 = indexQuantity.value_counts()
        df.drop(indexQuantity,inplace=True)
        print("Nb de lignes de données quantity <= 0: " + str(nbQuantity0))

        #Supprimer les lignes unitprice = 0
        indexUnitPrice = df[df['unitprice']<=0].index
        nbUnitPrice0 = indexUnitPrice.value_counts()
        df.drop(indexUnitPrice,inplace=True)
        print("Nb de lignes de données unitprice = 0: " + str(nbUnitPrice0))

        #Supprimer les lignes stockcode qui commence par une chaîne de caractère
        indexStockCode = df[df["stockcode"].str.match("^[A-Za-z]")==True].index
        nbStartChar = indexStockCode.value_counts()
        df.drop(indexStockCode,inplace=True)
        nbFinalData = df.shape[0]
        print("Nb de lignes de données stockcode commencant par une lettre: " + str(nbStartChar))

        # Mettre en Minuscule les lignes country EIRE -> Eire
        df['country'] = df['country'].str.title()
        # print(df['country'].unique())

        #Mettre les lignes avec country NULL ou Numérique en "unspecified"
        #si les autres colonnes ont un intérêt
        df.replace('NaN',np.nan)
        nbCountryNan = df['country'].isnull().sum()
        df['country'].fillna(value='Unspecified')
        print("Nb de lignes de données country vide: " + str(nbCountryNan))
        df['description'].fillna(value='Description du produit à intégrer')

        #Afficher le % de suppression et si <5% dire "envisageable"
        nbDeleteData = nbOriginalData - nbFinalData
        percFinalData = 100-((nbDeleteData*100)/nbOriginalData)
        print("Nb de lignes de données nettoyées: " + str(nbDeleteData))
        print("Pourcentage de données final: " + str(round(percFinalData,2)) + "%")

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(user=user,password=password,database_name=database_name)
        engine = create_engine(database_url, echo=False)

        #Transfert de la Dataframe dans une table temporaire de la BDD
        df.to_sql(Datatransfert._meta.db_table, if_exists='replace', con=engine, index=False)
        
        #Requête pour envoi data dans les différentes tables de la BDD
        sql = '''
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

        '''

        #Executer la requête pour envoi dans la BDD Postgre
        engine.execute(sql)


            # UPDATE dashboard_detailinvoice SET totalcost=unitprice*quantity;
from django.shortcuts import render, redirect
from django.http import HttpResponse
from dashboard.forms import InputFileForm
from dashboard.functions.functions import handle_uploaded_file   
from .models import *
from django.db.models import FloatField, Sum, Count
from django.db.models.functions import Cast
import json
import pandas as pd
from django.db import connection

# Create your views here.
def home(request):

    invoices = Invoice.objects.all().count()
    products = Product.objects.all().count()
    countries = Country.objects.all().count()

    # earningsfloat = DetailInvoice.objects.annotate(as_float=Cast('totalcost', FloatField())).aggregate(Sum('as_float'))
    # earnings = int(earningsfloat['as_float__sum'])

    context = {'invoices':invoices,'products':products,'countries':countries}

    return render(request,"dashboard/home.html", context)

def import_csv(request):  
    if request.method == 'POST':  
        csvFile = InputFileForm(request.POST, request.FILES)  
        if csvFile.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            return redirect('home')  
    else:  
        csvFile = InputFileForm()  
        return render(request,"dashboard/home.html",{'form':csvFile})

def dictfetchall(cursor):
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def sell_by_country(request):
    # sellbycountries = Country.objects.all().count()
    # sql = '''SELECT dashboard_invoice.country, detailinvoice_id, count(*) 
    #             FROM dashboard_detailinvoice 
    #             INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
    #             GROUP BY dashboard_invoice.country, detailinvoice_id
    #             ORDER BY count ASC 
    #             LIMIT 10'''
    # sql = "SELECT * FROM dashboard_country"
    # res = Country.objects.raw(sql)
    # sellbycountries = pd.DataFrame([item.__dict__ for item in res])
    # sellbycountries = DetailInvoice.objects.raw(sql)

    cursor = connection.cursor()
    cursor.execute('''SELECT dashboard_invoice.country, count(*) 
                            FROM dashboard_detailinvoice 
                            INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno 
                            GROUP BY dashboard_invoice.country
                            ORDER BY count DESC 
                            LIMIT 10''')

    # cursor.execute("SELECT dashboard_invoice.country, count(*) FROM dashboard_detailinvoice INNER JOIN dashboard_invoice ON dashboard_detailinvoice.invoiceno = dashboard_invoice.invoiceno GROUP BY dashboard_invoice.country")
    r = dictfetchall(cursor)
    # r = cursor.fetchall()


    cursor.close()
    
    return render(request, "dashboard/graphique-region.html", {'data': r})

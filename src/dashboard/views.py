from django.shortcuts import render, redirect
from django.http import HttpResponse
from dashboard.forms import InputFileForm
from dashboard.functions.functions import handle_uploaded_file   
from .models import *
from django.db.models import FloatField, Sum
from django.db.models.functions import Cast

# Create your views here.
def home(request):
    invoices = Invoice.objects.all().count()
    products = Product.objects.all().count()
    countries = Country.objects.all().count()

    earningsfloat = DetailInvoice.objects.annotate(as_float=Cast('totalcost', FloatField())).aggregate(Sum('as_float'))
    earnings = int(earningsfloat['as_float__sum'])

    context = {'invoices':invoices,'products':products,'countries':countries,'earnings':earnings}

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

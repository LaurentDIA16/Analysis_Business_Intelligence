from django.shortcuts import render, redirect
from django.http import HttpResponse
from dashboard.forms import InputFileForm
from dashboard.functions.functions import handle_uploaded_file   

# Create your views here.
def home(request):
    return render(request,"dashboard/home.html")

def import_csv(request):  
    if request.method == 'POST':  
        csvFile = InputFileForm(request.POST, request.FILES)  
        if csvFile.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            return redirect('home')  
    else:  
        csvFile = InputFileForm()  
        return render(request,"dashboard/home.html",{'form':csvFile})

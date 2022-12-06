from django import forms  

class InputFileForm(forms.Form):  
    file = forms.FileField() # for creating file input  
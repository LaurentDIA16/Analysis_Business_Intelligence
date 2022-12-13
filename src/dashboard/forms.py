from django import forms
from django.db import models

class InputFileForm(forms.Form): 
    file = forms.FileField(label='') # for creating file input  
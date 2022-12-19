from django import forms
from django.db import models


class InputFileForm(forms.Form): 
    file = forms.FileField(label='', widget=forms.FileInput(attrs={'accept': ".csv"})) # for creating file input  
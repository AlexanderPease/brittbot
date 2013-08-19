from django.db import models
from django.forms import ModelForm
import datetime

class Intro(models.Model):
    to_name = models.CharField(max_length=75, unique=False)
    to_email = models.EmailField(max_length=75, unique=False)
    for_name = models.CharField(max_length=75, unique=False)
    for_email = models.EmailField(max_length=75, unique=False)
    purpose = models.TextField(max_length=500, unique=False)
    sent = models.DateField(blank=True, null=True, unique=False) # Date the first email was sent
    connected = models.DateField(blank=True, null=True, unique=False) # Date the connection email was sent to both people


    def __unicode__(self):
        return "Connecting %s (%s) to %s (%s)" % (self.to_name, self.to_email, self.for_name, self.for_email)
    

class IntroForm(ModelForm):
    class Meta:
        model = Intro

    def __init__(self, *args, **kwargs):
        super(IntroForm, self).__init__(*args, **kwargs)
        self.fields['to_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Person to intro to'}
        self.fields['to_email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email'}
        self.fields['for_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Person asking for the intro'}
        self.fields['for_email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email'}
        self.fields['purpose'].widget.attrs = {'class': 'form-control', 'placeholder': 'Why he/she wants to connect', 'rows': '4'}


    
    
    



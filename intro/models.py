from django.db import models
from django import forms
from django.forms import ModelForm
import datetime

class Intro(models.Model):
    to_name = models.CharField(max_length=200, unique=True)
    to_email = models.CharField(max_length=200, unique=True)
    for_name = models.CharField(max_length=200, unique=True)
    for_email = models.CharField(max_length=200, unique=True)
    purpose = models.CharField(max_length=500, unique=True)
    sent = models.DateField(blank=True, null=True)
    connected = models.DateField(blank=True, null=True)


    def __unicode__(self):
        return "Connecting %s to %s" % (to_email, for_email)
    

##################################################################################
# Form Models
##################################################################################

class IntroForm(ModelForm):
    class Meta:
        model = Intro
        #def __init__(self, *args, **kwargs):
        #    super(CompanyForm, self).__init__(*args, **kwargs)
        #    self.fields['date'].widget = widgets.AdminDateWidget()


class CompanySearchForm(forms.Form): 
    name = forms.CharField(max_length=64, required=False)
    following = forms.BooleanField(required=False, initial=True)
    tracking= forms.BooleanField( required=False, initial=True)
    passed = forms.BooleanField(required=False, initial=True)
    no_status = forms.BooleanField(required=False, initial=True)
    #investor = forms.ChoiceField(required=False)
    min_raised = forms.IntegerField(required=False)
    max_raised = forms.IntegerField(required=False)

    
    
    



from django.db import models
from django import forms
from django.forms import ModelForm
import datetime

class Intro(models.Model):
    to_name = models.CharField(max_length=200)
    to_email = models.CharField(max_length=200)
    for_name = models.CharField(max_length=200)
    for_email = models.CharField(max_length=200)
    purpose = models.CharField(max_length=500)
    sent = models.DateField(blank=True, null=True) # Date the first email was sent
    connected = models.DateField(blank=True, null=True) # Date the connection email was sent to both people


    def __unicode__(self):
        return "Connecting %s (%s) to %s (%s)" % (to_name, to_email, for_name, for_email)
    

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

    
    
    



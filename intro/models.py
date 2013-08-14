from django.db import models
from django import forms
from django.forms import ModelForm
import datetime

class Intro(models.Model):
    to_name = models.CharField(max_length=75, unique=False)
    to_email = models.EmailField(max_length=75, unique=False)
    for_name = models.CharField(max_length=75, unique=False)
    for_email = models.EmailField(max_length=75, unique=False)
    purpose = models.CharField(max_length=500, unique=False)
    sent = models.DateField(blank=True, null=True, unique=False) # Date the first email was sent
    connected = models.DateField(blank=True, null=True, unique=False) # Date the connection email was sent to both people


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

# Not used
class CompanySearchForm(forms.Form): 
    to_name = forms.CharField(max_length=64)
    to_email = forms.EmailField()
    for_name = forms.CharField(max_length=64)

    following = forms.BooleanField(required=False, initial=True)
    tracking= forms.BooleanField( required=False, initial=True)
    passed = forms.BooleanField(required=False, initial=True)
    no_status = forms.BooleanField(required=False, initial=True)
    #investor = forms.ChoiceField(required=False)
    min_raised = forms.IntegerField(required=False)
    max_raised = forms.IntegerField(required=False)

    
    
    



from django.db import models
from django import forms
from django.forms import ModelForm
import datetime

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name
    

##################################################################################
# Form Models
##################################################################################

'''class CompanyForm(ModelForm):
    class Meta:
        model = Company
        def __init__(self, *args, **kwargs):
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.fields['date'].widget = widgets.AdminDateWidget()
'''

class CompanySearchForm(forms.Form): 
    name = forms.CharField(max_length=64, required=False)
    following = forms.BooleanField(required=False, initial=True)
    tracking= forms.BooleanField( required=False, initial=True)
    passed = forms.BooleanField(required=False, initial=True)
    no_status = forms.BooleanField(required=False, initial=True)
    #investor = forms.ChoiceField(required=False)
    min_raised = forms.IntegerField(required=False)
    max_raised = forms.IntegerField(required=False)

    
    
    



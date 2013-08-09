from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from django.core.context_processors import csrf
#import os.path # to find static files
from intro.models import Intro
import datetime

def index(request):
	if request.method == 'POST':
		to_name = request.POST.get('to_name')
		to_email = request.POST.get('to_email')
		for_name = request.POST.get('for_name')
		for_email = request.POST.get('for_email')
		purpose = request.POST.get('purpose')

		email_body = 'Hi %s, %s wants to meet with you to discuss %s. If you are open to the connection please <a href="#">click here</a>. If someone else should take this, please insert TBD' % (to_name, for_name, purpose) 

		connection_body = '%s meet %s. You two should chat about %s. Thanks!' % (to_name, for_name, purpose)

		#intro = Intro.objects.create(to_name=to_name, to_email=to_email, for_name=for_name, for_email=for_email, purpose=purpose)

		#return redirect
	return render_to_response('index.html', context_instance=RequestContext(request))

	
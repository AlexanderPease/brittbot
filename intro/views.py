from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from django.core.context_processors import csrf
from django.core.mail import send_mail
#import os.path # to find static files
from intro.models import Intro, IntroForm
import datetime


def index(request):
	form = IntroForm(request.POST) 

	if request.method == 'POST':
		# Valid form submitted
		if form.is_valid(): 
			intro = form.save() # Creates instance

			# Send initial email
			try:
				email_subject = "Intro to %s?" % intro.for_name
				email_body = 'Hi %s, %s wants to meet with you to discuss %s. If you are open to the connection please <a href="#">click here</a>. If someone else should take this, please insert TBD' % (intro.to_name, intro.for_name, intro.purpose) 
				send_mail(email_subject, email_body, EMAIL_HOST_USER, [intro.to_email], fail_silently=False)
				return redirect('/?sent=%s' % intro.to_name) # Always redirect after successful POST
			except:
				intro.delete()
				return render_to_response('index.html', {'form': form, 'error': 'Could not send email'}, context_instance=RequestContext(request))

		# POSTed form is not valid. This is just error handling
		else:
			return render_to_response('index.html', {'form': form, 'error': 'Model could not be created, check database'}, context_instance=RequestContext(request))
	# GET request
	else:
		sent = request.GET.get('sent')
		return render_to_response('index.html', {'form': form, 'sent': sent}, context_instance=RequestContext(request))

	
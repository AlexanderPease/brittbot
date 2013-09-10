from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from django.core.context_processors import csrf
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
#import os.path # to find static files
from intro.models import Intro, IntroForm
import datetime

RESPONSE_URL = 'http://brittbot.herokuapp.com/response/'

'''
Form for Brittany to fill out. Sends initial email request.
'''
def index(request):
	if request.method == 'POST':
		print 'POST'
		form = IntroForm(request.POST) 
		# Valid form submitted
		if form.is_valid(): 
			intro = form.save() # Creates instance
			# Send initial email
			try:
				email_subject = "Intro to %s?" % intro.for_name
				text_body = 'Hi %s, %s wants to meet with you to %s If you are open to the connection please email reply to brittany@usv.com. This will automatically generate an email from brittany@usv.com to connect the two of you. Thanks! Brittany' % (intro.to_name, intro.for_name, intro.purpose)
				html_body = 'Hi %s, %s wants to meet with you to %s </br></br>If you are open to the connection please <a href="%s%s">click here</a>. </br></br>This will automatically generate an email from brittany@usv.com to connect the two of you. </br></br> Thanks! Brittany' % (intro.to_name, intro.for_name, intro.purpose, RESPONSE_URL, intro.id)
				
				print "sending to: %s" % intro.to_email
				print "subject: %s" % email_subject
				print "body: %s" % text_body
				print "host: %s" % settings.EMAIL_HOST_USER

				msg = EmailMultiAlternatives(email_subject, text_body, settings.EMAIL_HOST_USER, [intro.to_email])
				msg.attach_alternative(html_body, "text/html")
				msg.send()

				print "email sent"
				intro.sent = datetime.date.today()
				intro.save()
				return redirect('/?sent=%s' % intro.to_name) # Always redirect after successful POST
			except:
				intro.delete()
				return render_to_response('index.html', {'form': form, 'error': 'Could not send email'}, context_instance=RequestContext(request))

		# POSTed form is not valid. This is just error handling
		else:
			return render_to_response('index.html', {'form': form, 'error': 'Model could not be created, check database'}, context_instance=RequestContext(request))
	# GET request
	else:
		form = IntroForm
		sent = request.GET.get('sent')
		return render_to_response('index.html', {'form': form, 'sent': sent}, context_instance=RequestContext(request))

'''
Handles response from the initial email.
Currently, the link emailed out modifies the database with a GET request, which is not ideal.
But there is no way to let most email client include a POST link (and for good reason). 
'''
def response(request, intro_id):
	try:
		intro = Intro.objects.get(id=intro_id)
	except:
		return render_to_response('response.html', {'error': "Sorry! I couldn't find this intro in my database. Please contact brittany@usv.com"}, context_instance=RequestContext(request))

	if intro.connected is not None:
		return render_to_response('response.html', {'error': "Your email has already been sent! Stop clicking the link!", 'intro': intro}, context_instance=RequestContext(request))

	email_subject = "%s <-> %s" % (intro.for_name, intro.to_name)
	email_body = 'Great that you guys are connecting!'
	send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [intro.to_email, intro.for_email], fail_silently=False)
	intro.connected = datetime.date.today()
	intro.save()
	return render_to_response('response.html', {'intro': intro}, context_instance=RequestContext(request))












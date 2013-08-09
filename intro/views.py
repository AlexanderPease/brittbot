from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, loader
from django.conf import settings #for STATIC_URL
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import os.path # to find static files
import datetime
from companies.models import Company, Investor, USV_Member, Correspondence, Note
from companies.models import CompanyForm, CompanySearchForm
from cb import investor_signal as cb

def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

''' Company database '''
def company_all(request):
	# If company_all has been POSTed to, it's to modify a company(s) currently in my search parameters
	if request.method == 'POST': 
		for pair in request.POST.items():
			company_name = pair[0]
			action = pair[1]
		
			if action and company_name != 'csrfmiddlewaretoken':
				company = Company.objects.get(name=company_name) #change to id
				# Follow
				if action == 'follow':
					company.interest = 5
					print "Following %s" % company_name
				# Track
				elif action == 'track':
					company.interest = 3
					print "Tracking %s" % company_name
				# Pass
				elif 'pass' in action:
					company.interest = 1
					# Notes
					note = None
					if 'sector' in action:
						note = 'Wrong sector'
					elif 'network' in action:
						note = 'No obvious network effects'
					elif 'stage' in action:
						note = 'Too late stage for USV'
					elif 'inactive' in action:
						note = 'Company is inactive/exited'
						company.exit = True
				
					if note: # write the note
						note = Note.objects.create(text = note, date = datetime.date.today(), company = company)
						print "Passed on %s with note: %s" % (company_name, note)
					else:
						print "Passed on %s" % company_name
				# Hide from viewable database
				elif action == 'hide':
					company.hidden = True
					print "Hid %s" % company_name
					
				company.save()
		
		
	form = CompanySearchForm(request.GET) 
	if form.is_valid():
		# Search by name
		companies = Company.objects
		name = form.cleaned_data['name']
		companies = companies.filter(name__contains=name)
		
		# Status
		following = form.cleaned_data['following']
		tracking = form.cleaned_data['tracking']
		passed = form.cleaned_data['passed']
		no_status = form.cleaned_data['no_status']
		# Default include all if none are included
		if not following and not tracking and not passed and not no_status:
			pass
		else:
			if not following:
				companies = companies.exclude(interest=5)
			if not tracking:
				companies = companies.exclude(interest=3)
			if not passed:
				companies = companies.exclude(interest=1)
			if not no_status:
				companies = companies.exclude(interest=None)
		
		# Filter by funding
		min_raised = form.cleaned_data['min_raised']
		max_raised = form.cleaned_data['max_raised']
		if max_raised or min_raised:
			if not max_raised:
				max_raised = 9999999999
			if not min_raised:
				min_raised = 0
			companies = companies.filter(total_raised__range=(min_raised, max_raised))
			print "Filtered funding by range ($%s, $%s)" % (min_raised, max_raised)
	
		'''OLD'''
		# Filter active/exited companies
		exit = request.GET.get('exit')
		if exit == 'false':
			companies = companies.filter(exit=False)
			print "Filtered for active companies only"
		elif exit == 'true':
			companies = companies.filter(exit=True)
			print "Filtered for exited companies only"
	
		# Filter USV companies
		portfolio = request.GET.get('portfolio')
		if portfolio == 'false':
			companies = companies.filter(portfolio=False)
			print "Filtered non-USV companies only"
		elif portfolio == 'true':
			companies = companies.filter(portfolio=True)
			print "Filtered USV companies only"
	
		# Filter based on investor
		investor = request.GET.get('investor')
		if investor:
			investor_query = Investor.objects.filter(name=investor)
			if len(investor_query) == 0:
				print "No Investors match the query"
			elif len(investor_query) > 1:
				print "More than one Investor matched the query"
			else:
				investor = investor_query[0]
				companies = companies.filter(investors__id=investor.id)
				print 'Filtered for %s portfolio' % investor
		
		# Filter based on date founded
		founded_after_month = request.GET.get('founded_after_month')
		founded_after_year = request.GET.get('founded_after_year')
		if founded_after_month and founded_after_year:
			founded_after = datetime.date(year=int(founded_after_year), month=int(founded_after_month), day=01)
		else:
			founded_after = datetime.date(year=1900, month=01, day=01)
	
		founded_before_month = request.GET.get('founded_before_month')
		founded_before_year = request.GET.get('founded_before_year')
		if founded_before_month and founded_before_year:
			founded_before = datetime.date(year=int(founded_before_year), month=int(founded_before_month), day=1)
		else:
			founded_before = datetime.date(year=2100, month=01, day=01)
		#companies = companies.filter(date_founded__range=(founded_after, founded_before))
		
		# Filter based on when company last raised capital
		last_raised_after_month = request.GET.get('last_raised_after_month')
		last_raised_after_year = request.GET.get('last_raised_after_year')
		if last_raised_after_month and last_raised_after_year:
			last_raised_after = datetime.date(year=int(last_raised_after_year), month=int(last_raised_after_month), day=01)
		else:
			last_raised_after = datetime.date(year=1900, month=01, day=01)
	
		last_raised_before_month = request.GET.get('last_raised_before_month')
		last_raised_before_year = request.GET.get('last_raised_before_year')
		if last_raised_before_month and last_raised_before_year:
			last_raised_before = datetime.date(year=int(last_raised_before_year), month=int(last_raised_before_month), day=1)
		else:
			last_raised_before = datetime.date(year=2100, month=01, day=01)
		#companies = companies.filter(recent_series_date__range=(last_raised_after, last_raised_before))
	
		# Filter out hidden/deleted companies. Default don't include hidden. 
		companies = companies.filter(hidden=False)
	
	
		# Sort the companies. Default alphabetical
		sort = request.GET.get('sort')
		if sort == 'recent_series':
			companies = companies.order_by('-recent_series') # - for descending
		elif sort == 'recent_series_date':
			companies = companies.order_by('-recent_series_date')
		elif sort == 'total_raised':
			companies = companies.order_by('total_raised')
		elif sort == 'investors':
			companies = companies.extra(select={'lower_name': 'lower(investors.name)'}).order_by('lower_name')
		else:
			companies = companies.extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
	
		# Include statistics to display. Paginator handles total number of companies
		companies_total = len(Company.objects.filter(hidden=False))
		companies_following = len(companies.filter(interest=5))
		companies_tracking = len(companies.filter(interest=3))
		companies_passed = len(companies.filter(interest=1))
		stats = {'following': companies_following, 
			'tracking': companies_tracking, 
			'passed': companies_passed, 
			'no_status': len(companies) - companies_following - companies_tracking - companies_passed,
			'total': companies_total}
		
	
		# Pagination of companies
		paginator = Paginator(companies, 25) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			companies = paginator.page(page)
		except PageNotAnInteger:
	    	# If page is not an integer, deliver first page.
			companies = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			companies = paginator.page(paginator.num_pages)
	
		# Include Investor models for search functions at top of page
		investors = Investor.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
		
		# Finally render the page
		return render_to_response('company_all.html', {'companies': companies, 'form':form,  'investors': investors, 'stats': stats, 'nav':'company'}, context_instance=RequestContext(request))
	
''' Form to add a company '''
def company_add(request):
	return company_form_processing(request)

''' Edit a company '''
def company_detail(request, company_id):
	company = get_object_or_404(Company, id=company_id)
	return company_form_processing(request, company=company)
	#company_form = CompanyForm(instance=company)
	#return render_to_response('company_edit.html', {'form': company_form}, context_instance=RequestContext(request))
	#return render_to_response('company_detail.html', {'company': company, 'nav':'company'}, context_instance=RequestContext(request))
	
''' Handles both editing an existing company and adding a new one 
     Arg company is passed in by company_edit() '''
def company_form_processing(request, company=None):
	# If the form has been submitted...
	if request.method == 'POST': 
		print request.POST
		# If there is already a company instance, this edits. If not, the form will create a new company instance
		form = CompanyForm(request.POST, instance=company) 
		
		# Valid form submitted
		if form.is_valid(): 
			company = form.save() # Creates Company model instance
			
			# Next action not handled by CompanyForm (bc I'm using a custom widget)
			next_action = request.POST.get('next_action')
			if next_action:
				datetime_var = datetime.datetime.strptime(next_action, '%Y-%m-%d')
				company.next_action = datetime_var.date()
			
			# Add a Note
			note = request.POST.get('note')
			if note:
				note = Note.objects.create(text = note, date = datetime.date.today(), company = company)
			
			# API searches
			#investorupdate_company(company)
			
			# Render index.html after successful use of form
			message =  "Saved to database"
			
			return redirect('/company/all/?message=success')
		
		# POSTed form is not valid. This is just error handling
		# ERROR HANDLING NEEDS TO BE UPDATED TO ACCOMODATE EDITING ERRORS (NOT JUST ADDING ERRORS)
		else:
			print form.errors # Form.errors won't pass through to template, no idea why. No one else seems to have this problem
			name = request.POST.get('name') #name = form.cleaned_data['name'] 'name' is missing for some reason
			try:
				company = Company.objects.get(name=name)
				if company:
					error = "Company '%s' already exists" % company.name
			except:
				error = 'Unknown'
			return render_to_response('company_form.html', {'form': form, 'error': error}, context_instance=RequestContext(request))
	
	# ...or form was not submitted, i.e. GET
	else:
		# Editing an existing company
		if company: 
			form = CompanyForm(instance=company)
			company = company
		# Adding a new company
		else:
			form = CompanyForm
			company = None
		return render_to_response('company_form.html', {'form': form, 'company': company}, context_instance=RequestContext(request))
		# There is probably a way to access all company from within the form, but I can't figure it out atm. So also passing company
	


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''Investor pages'''
def investor_all(request):
	investors = Investor.objects.all()
	investors = investors.exclude(name='Union Square Ventures')

	# Sort the companies. Default alphabetical
	sort = request.GET.get('sort')
	if sort == 'portfolio_size':
		investors = investors.order_by('portfolio_size')
	else:
		investors = investors.extra(select={'lower_name': 'lower(name)'}).order_by('lower_name') # case insensitive

	return render_to_response('investor_all.html', {'investors': investors, 'nav':'investor'}, context_instance=RequestContext(request))

def investor_detail(request, investor_name):
	investor = get_object_or_404(Investor, name=investor_name)


	return render_to_response('investor_detail.html', {'investor': investor, 'nav':'investor'}, context_instance=RequestContext(request))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''USV Member pages'''
def usv_member_all(request):
	usv_members = USV_Member.objects.all()
	return render_to_response('usv_member_all.html', {'usv_members': usv_members,'nav':'team'}, context_instance=RequestContext(request))

def usv_member_detail(request, usv_member_name):
	usv_member = get_object_or_404(USV_Member, name=usv_member_name)
	correspondences = usv_member.get_correspondences()

	# Filter companies based on portfolio
	portfolio = request.GET.get('portfolio')
	if portfolio == 'true':
		correspondences = correspondences.filter(company__portfolio=True)
	elif portfolio == 'false':
		correspondences = correspondences.filter(company__portfolio=False)
	
	# Quick filter for companies that didn't respond to initial email
	filter = request.GET.get('filter')
	if filter == "no_response":
		correspondences	= correspondences.filter(total_emails_out__gte=0, total_emails_in=None)
	
	# Sort the correspondences. Default latest email sent
	sort = request.GET.get('sort')
	if sort == 'company':
		correspondences = correspondences.order_by('company')
	elif sort == 'total_sent':
		correspondences = correspondences.order_by('-total_emails_out')
	elif sort == 'latest_received':
		correspondences = correspondences.order_by('-recent_email_in')
	elif sort == 'total_received':
		correspondences = correspondences.order_by('-total_emails_in')
	else:
		correspondences = correspondences.order_by('-recent_email_out')
		
	return render_to_response('usv_member_detail.html', {'usv_member': usv_member, 'correspondences': correspondences, 'nav':'team'}, context_instance=RequestContext(request))
	
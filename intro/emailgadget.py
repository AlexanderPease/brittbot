import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'usv_investor_signal.settings'
import imaplib, re, datetime
from models import Company, Investor, USV_Member, Correspondence

INBOX = "Inbox"
SENT = "[Gmail]/Sent Mail"

def email_login(account=None, password=None):
	if account and password:
		try:
			mail = imaplib.IMAP4_SSL('imap.gmail.com')
			result, message = mail.login(account, password)
			if result != 'OK':
				raise Exception
			return mail
		except:
			print "Failed to log into " + account
			exit()

'''Updates correspondence between company and usv_member
   Args should be Model instances. Does not need to include imaplib mailboxes instances'''
def update_email(company, usv_member, mail_inbox=None, mail_outbox=None):
	company_domain = company.get_domain()
	if not company_domain:
		print "Company %s domain name is unknown" % company
		return
	if usv_member.account and usv_member.password:
		# Log in if necessary
		if not mail_inbox or not mail_outbox:
			print "Logging into %s's account..." % usv_member
			mail_inbox = email_login(account=usv_member.account, password=usv_member.password)
			mail_inbox.select(INBOX, readonly=True) #mark as unread 
			mail_outbox = email_login(account=usv_member.account, password=usv_member.password)
			mail_outbox.select(SENT, readonly=True) #mark as unread 
			print 'Logged in as ' + usv_member.account
		
		
		# If no correspondence exists, create an instance
		try:
			correspondence_set = company.correspondence_set.filter(usv_member_id=usv_member.id)
			if len(correspondence_set) == 0:
				correspondence = None
				last_updated = None
			elif len(correspondence_set) > 1:
				print "Redundant correspondences in the database"
				raise Exception
			else:
				correspondence = correspondence_set[0]
				last_updated = correspondence.last_updated.strftime("%d-%B-%Y") # imaplib is very finnicky about format
		except:
			return
			
			
		# Emails received and sent. If correspondence already exists between company and usv_member, 
		# only search through usv_member's recent mail. If no correspondence exists, search through 
		#all mail (massive speed gains)
		raw_email_inbox = get_raw_emails(mail_inbox, sender=company_domain, recipient=usv_member.account, starting_date=last_updated)
		raw_email_outbox = get_raw_emails(mail_outbox, sender=usv_member.account, recipient=company_domain, starting_date=last_updated)
		
		# Add new emails to Correspondence instance
		if raw_email_inbox or raw_email_outbox:
			if not correspondence:
				correspondence = Correspondence.objects.create(usv_member=usv_member, company=company)
				print "First correspondence between %s and %s" % (usv_member, company)
			if raw_email_inbox:
				correspondence.recent_email_in = get_date(raw_email_inbox[-1])
				correspondence.total_emails_in = len(raw_email_inbox) + correspondence.total_emails_in # add to total
				print "Added new emails in from %s: %s total" % (company.name, correspondence.total_emails_in)
			if raw_email_outbox:
				correspondence.recent_email_out = get_date(raw_email_outbox[-1])
				correspondence.total_emails_out = len(raw_email_outbox) + correspondence.total_emails_out # add to total
				print "Added new emails out to %s: %s total" % (company.name, correspondence.total_emails_out)
			correspondence.last_updated = datetime.date.today()
			correspondence.save()
		print "Finished correspondence update between %s and %s" % (usv_member, company)
				
	

'''Iterates and updates email correspondences for all USV members and companies'''
def update_emails():
	for usv_member in USV_Member.objects.distinct():
		#Speeds up update_email() function
		print "Logging into %s's account..." % usv_member
		mail_inbox = email_login(account=usv_member.account, password=usv_member.password)
		mail_inbox.select(INBOX, readonly=True) #mark as unread 
		mail_outbox = email_login(account=usv_member.account, password=usv_member.password)
		mail_outbox.select(SENT, readonly=True) #mark as unread 
		print 'Logged in as ' + usv_member.account
		
		for company in Company.objects.distinct():
			update_email(company, usv_member, mail_inbox, mail_outbox)

'''def update_emails():
	# Iterate USV team members
	for usv_member in USV_Member.objects.distinct():
		if usv_member.password:
			mail_inbox = email_login(account=usv_member.account, password=usv_member.password)
			mail_inbox.select(INBOX, readonly=True) #mark as unread 
			mail_sent = email_login(account=usv_member.account, password=usv_member.password)
			mail_sent.select(SENT, readonly=True) #mark as unread 
			print 'Logged in as ' + usv_member.account

			# Iterate all companies
			for company in Company.objects.distinct():
				# Ensure Company model has an email address
				company_domain = company.get_domain()
				if company_domain:
					# Emails received and sent
					raw_email_inbox = get_raw_emails(mail_inbox, sender=company_domain, recipient=usv_member.account)
					raw_email_outbox = get_raw_emails(mail_sent, sender=usv_member.account, recipient=company_domain)
					
					# Only create Correspondence object if there are any emails
					if raw_email_inbox or raw_email_outbox:
						correspondence, created_bool = Correspondence.objects.get_or_create(usv_member=usv_member, company=company)
						if created_bool:
							print 'New correspondence with %s!!' % company.name #log for daily emails	
						if raw_email_inbox:
							correspondence.recent_email_in = get_date(raw_email_inbox[-1])
							correspondence.total_emails_in = len(raw_email_inbox)
							print "Emails in from %s: %s total" % (company.name, correspondence.total_emails_in)
						if raw_email_outbox:
							correspondence.recent_email_out = get_date(raw_email_outbox[-1])
							correspondence.total_emails_out = len(raw_email_outbox)
							print "Emails out to %s: %s total" % (company.name, correspondence.total_emails_out)
						correspondence.save()		
'''

'''Returns number of emails in mail_data'''
def get_mail_data_len(mail_data):
	if mail_data:
		return len(get_Mail_Data_List(mail_data))

'''Returns a list, each index is a raw email
   If no sender and recipient specified, defaults to ALL.
   mail is an impalib instance, other args are strings. Date must be in "01-Jan-2010" format'''
def get_raw_emails(mail, sender=None, recipient=None, starting_date=None):
	#print "get raw emails from %s to %s" %(sender, recipient)
	if mail and sender and recipient:
		search_string = __mailbox_search_string(sender, recipient, starting_date)
	elif mail:
		search_string = 'ALL'
	else:
		print 'get_raw_emails: passed NULL mail arg'
		return

	result, data = mail.search(None, search_string)
	ids = data[0] # data is a list. there is only data[0]
	id_list = ids.split() # ids is a space separated string

	raw_email_list = []
	for email_id in id_list:
		result, data = mail.fetch(email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
		raw_email = data[0][1] # here's the body, which is raw text of the whole email including headers and alternate payloads
		raw_email_list.append(raw_email)

	return raw_email_list

'''Parses raw email and returns date sent'''
import time
def get_date(raw_email=None):
	if raw_email:
		#Date: Mon, 5 Nov 2012 17:45:38 -0500
		date_string = re.search(r'[0-3]*[0-9] [A-Z][a-z][a-z] 20[0-9][0-9]', raw_email)
		time_obj = time.strptime(date_string.group(), "%d %b %Y")
		return datetime.date(time_obj.tm_year, time_obj.tm_mon, time_obj.tm_mday)
	else:
		print 'get_email_date: passed NULL raw_email arg'
		return

def __mailbox_search_string(sender, recipient, starting_date):
		if sender and recipient and starting_date:
			return "(FROM " + '"' + sender + '"' + ' TO "' + recipient + '"' + ' SINCE "' + starting_date + '"' + ")"
		elif sender and recipient:
			return "(FROM " + '"' + sender + '"' + ' TO "' + recipient + '"' + ")"
		

# Script
'''
mail_inbox = login()
mail_inbox.select(INBOX, readonly=True) #mark as unread 
mail_sent = login()
mail_sent.select(SENT, readonly=True) #mark as unread 
#result, mail_data = mail.search(None, '(FROM "brian@usv.com" TO "alexander@usv.com")') 
print get_Num_Emails(mail_inbox, 'brian@usv.com', ACCOUNT)
print get_Num_Emails(mail_sent, ACCOUNT, 'brian@usv.com')
'''




'''
print result
if result is 'OK':
	print 'OK'
	unclear why this isn't a string?
'''

'''
	ids = data[0] # data is a list. there is only data[0]
	id_list = ids.split() # ids is a space separated string. Returns a list of emails organized by id

	latest_email_id = id_list[-1]

	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

	raw_email = data[0][1] # here's the body, which is raw text of the whole email
	# including headers and alternate payloads
	print raw_email
'''


'''
import datetime
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))


date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date} HEADER Subject "My Subject" NOT FROM "yuji@grovemade.com")'.format(date=date))

'''
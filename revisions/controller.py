import datetime
import os
import tempfile


from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta

import revisions.settings as settings
# from revisions import settings
from revisions.models import Revision, EventDataDump, Event
from revisions.models import AppSettings, EmailList
from .utilities import dbisam_utility, diff_match_patch
from .utilities import send_update


def format_date(date):
	"""
		format a datime object for eventpath
		:date datetime object
		:return date string
	"""
	fmt = AppSettings.objects.get(field='REVISIONS_EVENTDATE_FMT')
	return date.strftime(fmt.value)
	# return date.strftime(settings.REVISIONS_EVENTDATE_FMT)

def get_date_range(start_date=None):
	"""
		Get the start and end date strings for the eventpath query
		:start_date datetime objects
		:return {end_date, start_date}
	"""	
	start_date = start_date or now()
	# delta = settings.REVISIONS_DATE_DELTA
	setting = AppSettings.objects.get(field='REVISIONS_DATE_DELTA')
	delta   = int(setting.value)
	return {
		'end_date': (timedelta(weeks=delta) + start_date),
		'start_date': start_date
	}

def fetch_events(date_range):
	"""
		Query Eventpath for events specified by date range
		:date_range {start_date: start-datetime, end_date: end-datetime}
		:return [{event}]
	"""
	# query = settings.REVISIONS_EVENT_QUERY
	# try:
	# 	results = dbisam_utility.query(query.format(**date_range), utility_path=settings.REVISIONS_DBISAM_UTILITY)	
	# except Exception, e:
	# 	raise e
	# return results
	utility_path = AppSettings.objects.get(field='REVISIONS_DBISAM_UTILITY')
	query        = AppSettings.objects.get(field='REVISIONS_EVENT_QUERY')
	date_field   = AppSettings.objects.get(field='REVISIONS_EVENTPATH_DATEFIELD')
	_query       = query.value.format(date_field=date_field.value, **date_range)	
	try:
		results = dbisam_utility.query(_query, utility_path=os.path.abspath(utility_path.value))	
	except Exception, e:
		raise e
	return results

def pretty_diff_html(old_text, new_text):
	"""
		compares two text and returns pretty html diff
		:old_text old-string
		:new_text new-string
		:return (html diff, change count)
	"""
	diff = diff_match_patch.diff_match_patch()
	changes = diff.diff_main(old_text, new_text)
	diff.diff_cleanupSemantic(changes)
	count = len([x for x in changes if x[0] == 1])
	return (diff.diff_prettyHtml(changes), count)


def lookup_event(event):
	return Event.objects.get_or_create(event_code=event['EventCode'], event_subcode=event['EventSubCode'])

def create_diff_html(event, note, status=None):
	# grab the last revision of the specific event

	revisions = Revision.objects.filter(event=event).order_by('update').reverse()
	if revisions:
		status = Revision.EXISTS
		diff, count = pretty_diff_html(revisions[0].event_note, note)		
		return diff, count, status
	else:
		status = Revision.NEW
		diff, count = pretty_diff_html(' ', note)		
		return diff, count, status

def add_revision(eventdatadump, event, raw_event_data):
	diff_html, count, status = create_diff_html(event, raw_event_data.get('Note'))

	# if the hash does not exist add the object
	# if there is no hash don't bother?
	Revision.objects.create(
		event=event,
		event_note=raw_event_data.get('Note') or "",
		update=eventdatadump,
		note_hash=Revision.hash_a_note(raw_event_data.get('Note')),
		diff_html=diff_html,
		count=count,
		status=status or Revision.NEW,
		update_by=raw_event_data.get("ModifiedUserID") or ""
	)
				
def parse_events(eventdatadump):
	"""
		Parse the returned events from update()
		Checks if a note hash exist in Revision, if none adds it
		:eventdatadump EventDataDump
		:return EventDataDump.timeupdated
	""" 
	_revised = False
	# loop through the event data stored in eventdatadump
	for raw_event_data in eventdatadump.event_data:
		event, _status = lookup_event(raw_event_data)
		# hash the note for the current event
		note_hash = Revision.hash_a_note(raw_event_data.get('Note'))
		# if the hash is not in Revision.objects already add it to Revision
		if not Revision.objects.filter(note_hash=note_hash).exists() and note_hash:
			_revised = True
			add_revision(eventdatadump, event, raw_event_data)
	
	if _revised:
		return eventdatadump

def update():
	"""
		Perform and update check on the Eventpath Events table
		Stores returned data in EventDataDump
		:return EventDataDump
	"""
	# query evetpath.events
	events = fetch_events(get_date_range())	
	if not events:
		return None
	# add the data to EventDataDump
	_update = EventDataDump.objects.create(event_data=events)
	return _update

def generate_update_link(update):
	# # revision/2014/Apr/3/
	# url_format = 'revision{:%Y/%b/%d/}'
	# return url_format.format(update.timestamp)
	return reverse('revisions_update', None, None, dict(update=update.pk))

def generate_email_body(update):
	context = {
		'updates': Revision.objects.filter(update=update), 
		'date_of_update': update.timestamp, 
		'date_range': get_date_range(start_date=update.timestamp)
	}
	return render_to_string('revisions/base_email.html', context)

def create_temp_file(update):
	# import tempfile
	file_name_format = "revision-{:%Y%m%d-%H%M%S}.html"
	html = generate_email_body(update)
	temp_dir = os.path.join(tempfile.gettempdir(), 'revisions')
	if not os.path.exists(temp_dir):
		os.mkdir(temp_dir)
	temp_file_name = file_name_format.format(update.timestamp)
	temp_file_path = os.path.join(temp_dir, temp_file_name)
	open(temp_file_path, 'w').write(html)
	return temp_file_path, html

def updates_log_msg(update):
	context = {}
	context['updates'] = Revision.objects.filter(update=update)

	msg_format = "{}-{} - changes {}"
	tmp_msg = []
	for x in context['updates']:
		tmp_msg.append(msg_format.format(x.event.event_code, x.event.event_subcode, x.count))

	return ("{} revisions found".format(context['updates'].count()), os.linesep.join(tmp_msg))

def email_update(update):

	email_message = generate_email_body(update)		

	sender = AppSettings.objects.get(field="REVISIONS_EMAIL_SENDER")
	recipients = [x.email for x in EmailList.objects.all() if x.active]

	if not recipients:
		print 'no recipients to email'
		raise Exception('No email recipents for update')
		return None

	msg = send_update.create_mime_msg(
		msg=email_message,
		subject="Revised Events for {:%d %b %Y %I:%M %p}".format(update.timestamp),
		sender=sender.value,
		recipients=recipients
	)
	send_update.send_mail(
		msg=msg, 
		user_login_creds=get_user, 
		sender=sender.value,
		recipients=recipients
	)

def get_user():
	from django.contrib.sessions.backends.base import SessionBase
	s = SessionBase()
	obj = AppSettings.objects.get(field="REVISIONS_KEY")
	return s.decode(obj.value)
	# return s.decode(settings.REVISIONS_KEY)


def main():
	# check for and store updated
	eventdatadump = update()
	if not eventdatadump:
		return None
	# store any revisions
	eventdatadump = parse_events(eventdatadump)
	if not eventdatadump:
		return None	
	# create the diffs
	# set the email context
	context = {'updates':Revision.objects.filter(update=eventdatadump)}
	# email template
	email_message = render_to_string('revisions/base_email.html', context)
	open('email.html', 'w').write(email_message)
	import webbrowser, os	
	webbrowser.open(os.path.abspath('./email.html'))


# revisions.json
# for k, v in revisions.iteritems():
# 	eventcode = k
# 	for sub, hashes in v.iteritems():
# 		subcode = sub
# 		for h, n in hashes.iteritems():
# 			if not h == 'event_data':
# 				_tmp = models.Revision.objects.create(
# 					event_code=eventcode,
# 					event_subcode=subcode,
# 					event_note=n.get('note') or "",
# 					# note_hash=h
# 				)
# 				_tmp.save()


# for k, v in revisions.iteritems():
# 	eventcode = k
# 	for sub, hashes in v.iteritems():
# 		subcode = sub
# 		for h, n in hashes.iteritems():
# 			if not h == 'event_data':				
# 				derp = dict(
# 					event_code=eventcode,
# 					event_subcode=subcode,
# 					event_note=n.get('note') or "")
# 				break

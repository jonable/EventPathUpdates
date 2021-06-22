import sys
import os
import webbrowser

from os import linesep
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

import taskbar
from revisions.models import Revision, EventDataDump
from revisions import controller
# from revisions import settings


class Command(BaseCommand):
	# args = '<poll_id poll_id ...>'
	option_list = BaseCommand.option_list + (
		make_option('--view_report', 
			dest='view_report',
			default='no',
			help='View report upon completion'),
		make_option('--email_report', 
			dest='email_report',
			help='Email report to list in revisions.settings'),	
		make_option('--notify_report', 
			dest="notify_report", 
			help="If True will display an operating system notification"),
	) 
	
	help = 'Check EventPath for updates made to Events'

	def handle(self, *args, **options):	
		self.stdout.write('Checking for events%s' % linesep) 

		eventdatadump = controller.update()
		# eventdatadump = EventDataDump.objects.get(id=55)
		if not eventdatadump:
			self.stdout.write('No events found between dates (start) - (end)%s' % linesep)
			return None
		
		self.stdout.write('Parsing events for any revisions%s' % linesep)
		# store any revisions		
		controller.parse_events(eventdatadump)		
		# set the email context
		context = {'updates':Revision.objects.filter(update=eventdatadump), 'date_of_update': eventdatadump.timestamp}
		# email template
		self.stdout.write('Creating Revisions Report%s' % linesep)
		
		email_message = render_to_string('revisions/base_email.html', context)		
		open('email.html', 'w').write(email_message)
		
		# handle reporting
		if options.get('view_report') == 'yes':
			webbrowser.open(os.path.abspath('./email.html'))

		if options.get('email_report'):
			controller.email_update(eventdatadump)

		if options.get('notify_report'):
				
			if context['updates'].count():
				init_message = controller.updates_log_msg(eventdatadump)				
				revision_html_file, html = controller.create_temp_file(eventdatadump)
			
			else:			
				init_message = ("No event revisions found", "no revisions found for {:%d %b %Y %I:%M %p}".format(eventdatadump.timestamp))
				revision_html_file = None

			taskbar.run(init_message=init_message, revision_html_file=revision_html_file)

		self.stdout.write('Update: %s complete %s' % (eventdatadump.timestamp, linesep))
		sys.exit()

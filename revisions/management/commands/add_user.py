# from optparse import make_option
from getpass import getpass

from django.contrib.sessions.backends.base import SessionBase as SB
from django.core.management.base import BaseCommand, CommandError

from revisions.models import AppSettings


class Command(BaseCommand):
	# option_list = BaseCommand.option_list + (
	# 	make_option('--view_report', 
	# 		dest='view_report',
	# 		default='no',
	# 		help='View report upon completion'),)

	def handle(self, *args, **options):	
		# move out of settings and into it's on file in appdata
		# if os.environ['OS'] == 'Windows_NT'
		# app_dir = os.path.join(os.environ['APPDATA'], 'revisions.com')
		# if not os.path.exist(app_dir):
		# 	os.mkdir(app_dir)		

		s = SB()		
		key, created = AppSettings.objects.get_or_create(field="REVISIONS_KEY")
		key.value = '%s' % s.encode([
			raw_input('Please enter your user login name: '), 
			getpass('Please enter your user login password: ')
			])
		key.save()	
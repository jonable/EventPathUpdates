import subprocess
import os 

from optparse import make_option


# from revisions import settings
from revisions.models import AppSettings

from django.core.management.base import BaseCommand, CommandError

interval_default = AppSettings.objects.get(field="REVISIONS_UPDATE_INTERVAL")

class Command(BaseCommand):


	option_list = BaseCommand.option_list + (
		make_option('--interval', 
			dest='interval',
			default=interval_default.value,
			help='View report upon completion'),
	)

	help = 'Schedule the the revisions task'

	def handle(self, *args, **options):	
		check_for_revisions_path = os.path.abspath('../bin/check_for_revisions.cmd')
		if not os.path.exists(check_for_revisions_path):
			print 'could not locate check_for_revisions.cmd at %s' % check_for_revisions_path
			return None

		subprocess.call([
			"SCHTASKS",
			"/CREATE",
			"/TN", "EventPathRevisionsShedule",
			"/TR", "\"{check_for_revisions_path}\"".format(check_for_revisions_path=check_for_revisions_path),
			"/SC", "HOURLY",
			"/MO", "{check_interval}".format(check_interval=options['interval']),
			"/ST", "09:00:00"]
		)

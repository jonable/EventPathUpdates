import json, os, datetime

from django.core.management.base import BaseCommand, CommandError

from revisions.models import Revision, EventDataDump, Event
from revisions import controller

def load_old_data():
	"""
		Convience method to load the old data stored in _data
	"""	
	from django.utils.timezone import utc
	# pull the dumps from _data
	ignore = ['data.json', 'revisions.json', 'store_notes.py', '.DS_Store', 'sertestdb', 'sertestdb', 'newsr.json']
	# file names are the timestamp from update
	# and load the json
	event_collection = [(float(x.split('.')[0]), json.load(open('../_data/%s' % x , 'r'))) for x in os.listdir('../_data') if x not in ignore]
	# loop over the dumps storing the data
	# kinda key store like
	_eventdatadump_pks = []
	for events in event_collection:
		timestamp = datetime.datetime.fromtimestamp(events[0], tz=utc)
		event_data = EventDataDump.objects.create(event_data=events[1])
		# need to overwrite timestamp because these were created in the past
		# not now and large part of the app relies on when event data is added
		event_data.timestamp = timestamp
		event_data.save()
		_eventdatadump_pks.append(event_data.pk)
	# include only most recent dumps incase data exist
	# was ordered_by 'timestamp' but i don't think that matters
	all_events = EventDataDump.objects.filter(pk__in=_eventdatadump_pks)
	# parse eventdatadumps for revisions
	for events in all_events:
		controller.parse_events(events)


class Command(BaseCommand):
	# args = '<poll_id poll_id ...>'
	help = 'Load data stored in _data'

	def handle(self, *args, **options):
		# self.stdout.write('%s %s' % (args, options))
		
		inpt = raw_input('You are about to delete all data in EventDataDump, Event, Revision: enter ok to continue...')
		if not inpt == 'ok':
			return None
			
		EventDataDump.objects.all().delete()
		Event.objects.all().delete()
		Revision.objects.all().delete()

		self.stdout.write('loading data from %s \n' % (os.path.abspath('../_data')))
		load_old_data()
		# # self.stdout.write('parsing data for revisions \n')
		# # load_old_revisions()
		self.stdout.write('databse data loaded \n')






import wx, os

if __name__ == '__main__':
	abspath = os.path.abspath(__file__)
	dname   = os.path.dirname(abspath)
	os.chdir(dname)	
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventupdates.settings")

from revisions.models import Revision, EventDataDump
from revisions import controller
from wxapp.taskbar import RevisionsTaskBarIcon

def fetch_latest(icon):
	context = {}
	eventdatadump = EventDataDump.objects.latest('pk')
	context['updates'] = Revision.objects.filter(update=eventdatadump)
	
	if context['updates'].count():
		init_message = controller. updates_log_msg(eventdatadump)
		icon.revision_html_file, html = controller.create_temp_file(eventdatadump)
	else:
		init_message = ("No event revisions found", "no revisions found for {:%d %b %Y %I:%M %p}".format(eventdatadump.timestamp))
		icon.revision_html_file = None

	icon.ShowBalloon(*init_message)
	if icon.revision_html_file:
		icon.launch_browser()

def run(*args, **kwargs):
	app = wx.App()
	icon = RevisionsTaskBarIcon(*args, **kwargs)	
	icon.fetch_latest = fetch_latest
	app.MainLoop()


if __name__ == '__main__':

	# default_bubble_title = "Revised Events for {:%d %b %Y %I:%M %p}".format(update.timestamp)
	# context = {}

	# # eventdatadump = EventDataDump.objects.get(pk=34)
	# eventdatadump = EventDataDump.objects.latest('pk')
	# context['updates'] = Revision.objects.filter(update=eventdatadump)
	
	# if context['updates'].count():
	# 	init_message = controller. updates_log_msg(eventdatadump)
	# 	revision_html_file, html = controller.create_temp_file(eventdatadump)
	# else:
	# 	init_message = ("No event revisions found", "no revisions found for {:%d %b %Y %I:%M %p}".format(eventdatadump.timestamp))
	# 	revision_html_file = None
	run()
	# run(init_message=init_message, revision_html_file=revision_html_file)    


import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.utils.timezone import now, timedelta
from django.views.generic.dates import DayArchiveView, MonthArchiveView
from django.views.generic.dates import YearArchiveView, ArchiveIndexView
from django.views.decorators.csrf import csrf_exempt


from revisions.models import EventDataDump, Revision, Event

class UpdateDayArchiveView(DayArchiveView):
	queryset         = EventDataDump.objects.all()
	date_field       = "timestamp"
	make_object_list = True
	allow_future     = False

class UpdateMonthArchiveView(MonthArchiveView):
	queryset         = EventDataDump.objects.all()
	date_field       = "timestamp"
	make_object_list = False
	allow_future     = True

class UpdateYearArchiveView(YearArchiveView):
	queryset         = EventDataDump.objects.all()
	date_field       = "timestamp"
	make_object_list = False
	allow_future     = True

class UpdateIndexArciveView(ArchiveIndexView):
	queryset         = EventDataDump.objects.all()
	date_field       = "timestamp"
	make_object_list = False
	allow_future     = True

def view_email(request, update):
	update = EventDataDump.objects.get(pk=update)
	return render_to_response("revisions/base_email.html", {
		'updates': Revision.objects.filter(update=update), 
		'date_of_update': update.timestamp
	})	

def update(request, update):

	# update = datetime.fromtimestamp(float(update), tz=utc)		
	update = EventDataDump.objects.get(pk=update)
	return render_to_response("revisions/update.html", {
		'updates': Revision.objects.filter(update=update), 
		'date_of_update': update.timestamp
	})	

def event_history(request, event_id):
	revised = Revision.objects.filter(event__pk=event_id)
	return render_to_response("revisions/_event.html", {
		'revised': revised.order_by('update').reverse(), 
		'event': revised[0].event
	})	

def daily_digest(request):
	today = now().date()
	tomorrow = today + timedelta(days=1)
	updates = EventDataDump.objects.filter(timestamp__lte=tomorrow, timestamp__gte=today)
	events = {}
	for update in updates:
		if update.revision_set.count():
			for revision in update.revision_set.iterator():
				if not events.has_key(revision.event.id):
					events[revision.event.id] = revision.event
					events[revision.event.id].update_id = revision.id 
					events[revision.event.id].count = revision.count
				else:
					events[revision.event.id].count += revision.count 
	
	context = {}
	context['events'] = events.values()
	context['todays_date'] = today	
	return render(request, 'revisions/daily_digest.html', context)


def revisions_day(request, month=None, day=None, year=None, *args, **kwargs):
	_day       = UpdateDayArchiveView()
	_day.year  = year
	_day.month = month
	_day.day   = day
	date_list, object_list, extra_context = _day.get_dated_items()

	for x in object_list:
		x.count = Revision.objects.filter(update=x).count()

	return render(request, 'revisions/eventdatadump_archive_day.html', dict(object_list=object_list, **extra_context))

def revisions_menu(request, *args, **kwargs):
	active_month = None
	active_year  = None
	if not kwargs.has_key('year'):
		kwargs['year'] = "%s" % now().year

	if kwargs.has_key('month'):
		month       = UpdateMonthArchiveView()
		month.month = kwargs.get('month')
		month.year  = kwargs.get('year')
		days_list, items, extra_context = month.get_dated_items()
		active_month = extra_context['month']

	if kwargs.has_key('year'):
		year      = UpdateYearArchiveView()
		year.year = kwargs.get('year')		
		months_list, items, extra_context = year.get_dated_items()
		active_year = extra_context['year']

	index = UpdateIndexArciveView()
	years_list, items, extra_context = index.get_dated_items()
	menu = {'years': []}
	

	for _year in sorted(years_list):
		if active_year and str(_year.year) == active_year:
			_tmp_year = {
				'year': _year.year,
				'is_active': True,
				'months': []
			}
			for _month in sorted(months_list):
				if active_month and active_month.month == _month.month:
					_tmp_month = {
						'is_active': 'True',
						'month':  _month.strftime("%b"),
						'days': sorted(days_list)
					}
				else:
					_tmp_month = {
						'is_active': False,
						'month':  _month.strftime("%b")
					}
				_tmp_year['months'].append(_tmp_month)
		else:
			_tmp_year = {
				'year': _year.year,
				'is_active': False,
			}
		menu['years'].append(_tmp_year)

	return render(request, 'revisions/revisions_archive_menu.html', {'menu': menu})

@csrf_exempt
def ajax_search(request):
	from django.db.models import Q
	import json	
	e = Event.objects.filter(
		Q(event_code__icontains=request.POST['query']) | Q(description__icontains=request.POST['query'])
	)
	if e.count():
		j = json.dumps({'search_results': [dict( 
			 description=x.description,
			 event_code=x.event_code,
			 event_subcode=x.event_subcode,
			 id=x.id) for x in e]})
		return HttpResponse(j , content_type="application/json")
	
	return HttpResponse(json.dumps({'search_results': None}), content_type="application/json")
	
	# return HttpResponse(json.dumps(request.POST), content_type="application/json")

from hashlib import md5
from django.db import models
from jsonfield import JSONField


class EventDataDump(models.Model):
	"""Simple storage for date returned during an update"""
	timestamp    = models.DateTimeField('Created Date', auto_now=False, auto_now_add=True)	
	event_data   = JSONField('Event Data')

	def __unicode__(self):
		return '{:%a %d %b, %Y %I:%m %p}'.format(self.timestamp)

	# def remove_empty_events(self):
	# 	""" remove EventDataDumps without a revision bound to it """
	# 	[x.delete() for x in EventDataDump.objects.all() if not x.revision_set.count()]

class Event(models.Model):
	"""Represents an Event in EventPath"""
	event_code      = models.CharField('Event Code', max_length=100)
	event_subcode   = models.CharField('Event SubCode', max_length=100)
	description 	= models.TextField('Description', blank=True)

	def __unicode__(self):
		return "%s %s" % (self.event_code, self.event_subcode)

class Revision(models.Model):
	"""Revision object for revisised notes."""
	REMOVED    = 0
	NEW        = 1
	EXISTS     = 2
	
	event      = models.ForeignKey(Event)
	event_note = models.TextField('Event Note')
	note_hash  = models.CharField('Note Hash', max_length=200)	
	diff_html  = models.TextField('Event Note Diff Html', blank=True)	
	status     = models.IntegerField('Revision Status', choices=((REMOVED, 'removed'), (EXISTS, 'exists'), (NEW, 'new')), default=NEW, max_length=3)
	count      = models.IntegerField('Number of changes', max_length=5)
	update     = models.ForeignKey(EventDataDump)
	update_by  = models.CharField('Updated By', max_length=200, blank=True)
	timestamp  = models.DateTimeField('Created Date', auto_now=False, auto_now_add=True)

	#Overriding
	def save(self, *args, **kwargs):	
		# if there is an event note and the hash has not been set
		if len(self.event_note) and not self.note_hash:
			self.note_hash = self.__class__.hash_a_note(self.event_note)
		super(Revision, self).save(*args, **kwargs)

	def __unicode__(self):
		return "{} - {:%d/%m/%y %I:%H %p}".format(self.event.event_code, self.update.timestamp)

	@classmethod
	def hash_a_note(cls, note):
		if note:
			return md5(str(note)).hexdigest() 

	def get_absolute_url(self):
		return "/revision/event/{}/".format(self.pk)

class AppSettings(models.Model):
	field = models.CharField('Field Name', max_length=100, unique=True)
	value = models.CharField('Value', max_length=200)
	description = models.TextField('Description', blank=True)

	def __unicode__(self):
		return self.field

class EmailList(models.Model):
	name   = models.CharField('Name', max_length=100)
	email  = models.CharField('Email', max_length=100)
	active = models.BooleanField('Active', default=False)

	def __unicode__(self):
		return self.email	






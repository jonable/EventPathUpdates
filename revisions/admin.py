from django.contrib import admin
from django.db.models import Q

from revisions.models import Event, Revision, EventDataDump
from revisions.models import EmailList, AppSettings

class EventAdmin(admin.ModelAdmin): pass
class RevisionAdmin(admin.ModelAdmin): pass
class EventDataDumpAdmin(admin.ModelAdmin): pass

admin.site.register(Event, EventAdmin)
admin.site.register(EventDataDump, EventDataDumpAdmin)
admin.site.register(Revision, RevisionAdmin)




# class RevisionAdmin(admin.ModelAdmin): pass
# class EventAdmin(admin.ModelAdmin): pass
# class EventDataDumpAdmin(admin.ModelAdmin): pass
class EmailListAdmin(admin.ModelAdmin): 
	list_display = ('email', 'active')
	list_editable = ('active',)
	
class AppSettingsAdmin(admin.ModelAdmin): 
	list_display = ('field', 'description','value')
	
	def queryset(self, request):
		qs = super(AppSettingsAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(~Q(field="REVISIONS_KEY"))	

# admin.site.register(Revision, RevisionAdmin)
# admin.site.register(Event, EventAdmin)
# admin.site.register(EventDataDump, EventDataDumpAdmin)
admin.site.register(EmailList, EmailListAdmin)
admin.site.register(AppSettings, AppSettingsAdmin)

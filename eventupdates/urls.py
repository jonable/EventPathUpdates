from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    url(r'^revision/(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d+)/$',
        'revisions.views.revisions_day',
        name="revision_day"
    ),    
    url(r'^revision/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
       'revisions.views.revisions_menu',
        name="revisions_menu"
    ),    
    url(r'^revision/(?P<year>\d{4})/$',
       'revisions.views.revisions_menu',
        name="revisions_menu"
    ), 
    url(r'^revision/$',
       'revisions.views.revisions_menu',
        name="revisions_menu"
    ),        

    url(r"^revision/update/(?P<update>\d+)/", 
        'revisions.views.update', name='revisions_update' ),

    url(r"^revision/update/email/(?P<update>\d+)/", 
        'revisions.views.view_email'),

    url(r"^revision/event/(?P<event_id>\d+)/", 
        'revisions.views.event_history', name='revisions_eventhistory'),

    url(r"^revision/digest/$", 
        'revisions.views.daily_digest', name='revisions_digest'),

    url(r"^revision/search$", 'revisions.views.ajax_search', name="revisions_ajax_search"),

    url(r'^admin/', include(admin.site.urls)),

)

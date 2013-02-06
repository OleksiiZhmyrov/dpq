from django.conf.urls import patterns, include, url
from queue.views import *
from django.contrib.auth.views import login
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', queue),
    (r'^history/$', history),
    (r'^charts/$', charts),
    (r'^help/$', 'django.views.generic.simple.direct_to_template', {'template' : 'dpq_help.html'}),
    (r'^update/create/$', create_queue_item),
    (r'^update/refresh/(?P<current_tab>\w{0,32})/$', refresh),
    (r'^update/fetch/$', fetch_queue_item),
    (r'^update/modify/$', modify_queue_item),
    (r'^update/superusers/$', fetch_superusers_list),
    (r'^login/$', login),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
)

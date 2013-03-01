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
    (r'^ajax/request/key/$', request_key),
    (r'^ajax/create/$', create_queue_item),
    (r'^ajax/request/fetch/$', fetch_queue_item),
    (r'^ajax/request/info/(?P<item_id>[0-9a-f]{32})/$', fetch_push_details),
    (r'^ajax/modify/$', modify_queue_item),
    (r'^ajax/request/superusers/$', fetch_superusers_list),
    (r'^ajax/request/visualisation/average/$', visualisation_average),
    (r'^ajax/request/visualisation/branch/(?P<branch>\w{0,32})/(?P<mode>\w{0,15})/$', visualisation_branch_duration),
    (r'^ajax/admin/invalidate-cache/$', invalidate_application_cache),
    (r'^ajax/refresh-branch/(?P<branch>\w{0,32})/$', refresh_branch),
    (r'^login/$', login),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
)

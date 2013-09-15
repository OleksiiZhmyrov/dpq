from django.conf.urls import patterns, include
from django.contrib.auth.views import login
from django.conf import settings
from django.contrib import admin

from queue.views import *


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', queue),
                       (r'^maintenance/$', maintenance_page),
                       (r'^history/(?P<branch>\w{0,32})/$', history),
                       (r'^charts/$', charts),
                       (r'^help/$', help_page),
                       (r'^search/$', search_page),
                       (r'^cards/$', kanban_cards),
                       (r'^ajax/search/$', search_results),
                       (r'^ajax/request/key/$', request_key),
                       (r'^ajax/create/$', create_queue_item),
                       (r'^ajax/request/fetch/$', fetch_queue_item),
                       (r'^ajax/request/jirastory/$', get_story_data_from_JIRA),
                       (r'^ajax/request/info/(?P<item_id>[0-9a-f]{32})/$', fetch_push_details),
                       (r'^ajax/modify/$', modify_queue_item),
                       (r'^ajax/move/$', move_queue_item),
                       (r'^ajax/request/superusers/$', fetch_superusers_list),
                       (r'^ajax/request/heroes/$', heroes_and_villains),
                       (r'^ajax/request/visualisation/average/$', visualisation_average),
                       (r'^ajax/request/visualisation/branch/(?P<branch>\w{0,32})/(?P<mode>\w{0,15})/$',
                        visualisation_branch_duration),
                       (r'^ajax/admin/invalidate-cache/$', invalidate_application_cache),
                       (r'^ajax/refresh-branch/(?P<branch>\w{0,32})/$', refresh_branch),
                       (r'^api/branch/status/update/$', api_update_branch_status),
                       (r'^api/branch/status/$', api_get_branches_statuses),
                       (r'^api/cards/download/$', api_download_cards),
                       (r'^api/joker/$', api_joker),
                       (r'^api/joker/$', api_joker),
                       (r'^login/$', login),
                       (r'^logout/$', logout_page),
                       (r'^register/$', register_page),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^admin/', include(admin.site.urls)),
)

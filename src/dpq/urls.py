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
                       (r'^retro/$', retro_boards_list),
                       (r'^retro/(?P<sprint>[0-9]{1,2})/(?P<team>[a-zA-Z]{1,32})/$', retro_boards_sprint),
                       (r'^ci/deskcheck/$', ci_display_deskcheck),
                       (r'^ci/outdated_stories/$', ci_display_outdated_stories),
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
                       (r'^ajax/request/visualisation/daily/$', visualization_daily_pushes),
                       (r'^ajax/request/visualisation/branch/(?P<branch>\w{0,32})/(?P<mode>\w{0,15})/$',
                        visualisation_branch_duration),
                       (r'^ajax/admin/invalidate-cache/$', invalidate_application_cache),
                       (r'^ajax/refresh-branch/(?P<branch>\w{0,32})/$', refresh_branch),
                       (r'^api/branch/status/update/$', api_update_branch_status),
                       (r'^api/branch/status/$', api_get_branches_statuses),
                       (r'^api/cards/download/$', api_download_cards),
                       (r'^api/joker/$', api_joker),
                       (r'^api/retro/(?P<sprint>[0-9]{1,2})/(?P<team>[a-zA-Z]{1,32})/$', retro_board_table_contents),
                       (r'^api/retro/sticker/add/$', retro_board_add_sticker),
                       (r'^api/retro/sticker/voteup/$', retro_board_voteup_sticker),
                       (r'^api/retro/sticker/remove/$', retro_board_remove_sticker),
                       (r'^api/retro/sticker/fetch/$', retro_board_fetch_sticker),
                       (r'^api/retro/sticker/modify/$', retro_board_modify_sticker),
                       (r'^login/$', login),
                       (r'^logout/$', logout_page),
                       (r'^register/$', register_page),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^admin/', include(admin.site.urls)),
)

# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from queue.models import *


admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(QueueRecord)
admin.site.register(UserStory)
admin.site.register(Statistics)
admin.site.register(Branch)
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(CustomUserRecord)
admin.site.register(Sprint)
admin.site.register(RetroBoard)
admin.site.register(BoardSticker)

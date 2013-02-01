# -*- coding: utf-8 -*-

from queue.models import *
from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(Queue)
admin.site.register(Statistics)
admin.site.register(Branch)

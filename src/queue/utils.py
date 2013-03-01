from datetime import datetime
from django.core.cache import cache
from django.http import Http404
from hashlib import sha1
from queue.models import *
import logging

logger = logging.getLogger('django.db.backends')


def log_info(message):
    now = datetime.now()
    logger.info('[' + now.strftime('%d/%b/%Y %H:%M:%S') + '] ' + message)


def update_key():
    key = hash(datetime.now())
    cache.set('key', key)


def get_last_pushes_for_branch(branch_name):
    if (get_cached_data(branch_name) == None):
        log_info('Updating tab for branch ' + branch_name + ' from database')
        branch_obj = Branch.objects.get(name=branch_name)
        push_table = Queue.objects.filter(branch=branch_obj,
                                          status__in=[Queue.WAITING, Queue.IN_PROGRESS]).order_by('-index')
        cache.set(branch_name, push_table)
        return push_table
    else:
        log_info('Using cached data to update tab for branch' + branch_name)
        return get_cached_data(branch_name)


def get_cached_data(field):
    return cache.get(field)


def invalidate_cache():
    cache.clear()


def get_active_branches():
    if(get_cached_data('active_branches') == None):
        try:
            active_branches = Branch.objects.filter(is_active=True)
            cache.set('active_branches', active_branches)
            return active_branches
        except Branch.DoesNotExist:
            return None
    else:
        return get_cached_data('active_branches')
    

def get_item_by_id(id):
    try:
        item = Queue.objects.get(queue_id=id)
        return item
    except Queue.DoesNotExist:
        raise Http404(u'Queue item with selected id does not exist.')


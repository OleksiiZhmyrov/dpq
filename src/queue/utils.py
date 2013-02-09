from datetime import datetime
from django.core.cache import cache
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


def get_items_list():
    if (get_cached_data('queue_list') == None):
        log_info('Update cached queue list from DB')
        
        queue_list = Queue.objects.order_by('-index')[:29]
        cache.set('queue_list', queue_list)
        update_key()
        
        return queue_list
    else:
        logger.debug('Getting queue data from cache')
        return get_cached_data('queue_list')


def get_cached_data(field):
    data = {'queue_list' : cache.get('queue_list'),
            'key' : cache.get('key'),
            'active_branches' : cache.get('active_branches'),
           }
    return data[field]

def invalidate_cache():
    cache.set_many({'queue_list' : None,
                    'key' : None,
                    'active_branches' : None})


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
        raise DoesNotExist

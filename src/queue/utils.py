from datetime import datetime
import logging
from datetime import date

from django.core.cache import cache
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from queue.models import *


logger = logging.getLogger('django.db.backends')


def log_info(message):
    """

    :param message:
    """
    now = datetime.now()
    logger.info('[' + now.strftime('%d/%b/%Y %H:%M:%S') + '] ' + message)


def update_key():
    """


    """
    key = hash(datetime.now())
    cache.set('key', key)


def get_last_pushes_for_branch(branch_name):
    """

    :param branch_name:
    :return:
    """
    if get_cached_data(branch_name) is None:
        log_info('Updating tab for branch ' + branch_name + ' from database')
        branch_obj = Branch.objects.get(name=branch_name)
        push_table = Queue.objects.filter(branch=branch_obj,
                                          status__in=[Queue.WAITING, Queue.IN_PROGRESS]).order_by('-index')
        cache.set(branch_name, push_table)

    else:
        log_info('Using cached data to update tab for branch ' + branch_name)
        push_table = get_cached_data(branch_name)

    if len(push_table) != 0:
        first_item = push_table[len(push_table) - 1].index
        last_item = push_table[0].index
    else:
        first_item = last_item = 0

    return {'push_table': push_table,
            'first_item': first_item,
            'last_item': last_item}


def get_cached_data(field):
    """

    :param field:
    :return:
    """
    return cache.get(field)


def invalidate_cache():
    """


    """
    cache.clear()


def get_teams():
    try:
        teams = Team.objects.all()
        return teams
    except Team.DoesNotExist:
        return None


def get_active_branches():
    """


    :return:
    """
    if get_cached_data('active_branches') is None:
        try:
            active_branches = Branch.objects.filter(is_active=True)
            cache.set('active_branches', active_branches)
            return active_branches
        except Branch.DoesNotExist:
            return None
    else:
        return get_cached_data('active_branches')


def get_item_by_id(item_id):
    """
        Gets Queue object from database by item_id.
        Returns found object or redirects to 404 page.

    :param item_id:
    :return: :raise:
    """
    try:
        item = Queue.objects.get(queue_id=item_id)
        return item
    except Queue.DoesNotExist:
        raise Http404(u'Queue item with selected id does not exist.')


def update_daily_statistics(push_duration):
    """
        Adds push timing to daily statistics.
        Returns nothing.

    :param push_duration:
    """
    try:
        statistics_day = Statistics.objects.get(date=date.today())
    except ObjectDoesNotExist:
        statistics_day = Statistics(date=date.today())

    statistics_day.number_of_pushes += 1
    statistics_day.total_push_duration += int(push_duration)

    statistics_day.save()


def shift_indexes(first, second):
    """
        Shifts indexes of two Queue objects.
        Returns nothing.

    :param first:
    :param second:
    """
    first_index = first.index
    second_index = second.index

    first.index = 0
    first.save()

    second.index = first_index
    second.save()

    first.index = second_index
    first.save()

    invalidate_cache()
    update_key()

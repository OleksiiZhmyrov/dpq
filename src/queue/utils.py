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
        push_table = QueueRecord.objects.filter(branch=branch_obj,
                                                status__in=[QueueRecord.WAITING, QueueRecord.JOKER_MODE,
                                                            QueueRecord.IN_PROGRESS]).order_by('index')
        custom_user_records = CustomUserRecord.objects.all()
        trump_cards = dict([(cur.django_user.id, cur.trump_cards) for cur in custom_user_records])

        for item in push_table:
            item.trump_cards = trump_cards.get(item.owner.id, 0)

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
    update_key()


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
        item = QueueRecord.objects.get(queue_id=item_id)
        item.trump_cards = CustomUserRecord.objects.get(django_user_id=item.owner.id).trump_cards
        return item
    except QueueRecord.DoesNotExist:
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


def get_slowest_push_id(input):
    array = []

    for item in input.values_list('push_date', 'done_date', 'queue_id'):
        array.append(item)

    for index in range(len(array)):
        moved = False

        for bubble in reversed(range(index + 1, len(array))):
            if array[bubble - 1][1] - array[bubble - 1][0] > array[bubble][1] - array[bubble][0]:
                array[bubble], array[bubble - 1] = array[bubble - 1], array[bubble]
                moved = True

        if not moved:
            break

    return array[-1][2]


def change_branch_status(branch, status):
    if status == "success":
        branch.build_success = True
    elif status == "failure":
        branch.build_success = False
    branch.save()
    invalidate_cache()
    log_info(" === Status for branch {branch_name} is changed to {branch_status}".format(
        branch_name=branch.name, branch_status=status))
    response = {'status': 'OK'}
    return branch, response


def add_voters_list_to_stickers(stickers):
    for sticker in stickers:
        if sticker.voters is not None:
            voters_ids_list = sticker.voters.split(";")
            voters = User.objects.filter(id__in=voters_ids_list)
            sticker.voters_string = ", ".join(str(x.username) for x in voters)
    return stickers


def finalize_active_pushes(branch):
    queue_list = QueueRecord.objects.filter(branch=branch, status=QueueRecord.IN_PROGRESS)
    for item in queue_list:
        item.done_date = datetime.now()
        item.status = QueueRecord.DONE
        item.save()
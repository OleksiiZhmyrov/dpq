from datetime import datetime, timedelta
from exceptions import TypeError
from json import loads, dumps
from uuid import uuid1
from django.views.decorators.csrf import csrf_exempt
from jira import *

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from queue.forms import *
from queue.models import *
from django.db.models import Q, Count
from queue.paginators import DiggPaginator
from queue.utils import *


def queue(request):
    """

    :param request:
    :return: :raise:
    """
    try:
        current_tab = get_active_branches()[0].name
    except IndexError:
        raise Http404(u'No active branches.')
    return render_to_response('queue/dpq_queue.html',
                              RequestContext(request, {'current_tab': current_tab,
                                                       'active_branches': get_active_branches()}))


def refresh_branch(request, branch):
    """

    :param request:
    :param branch:
    :return:
    """
    return render_to_response('queue/dpq_queue_table_branch_tab.html',
                              RequestContext(request, {'data': get_last_pushes_for_branch(branch),
                                                       'branch': branch,
                                                       'jira_browse_url': JIRA_BROWSE_URL}))


def request_key(request):
    """

    :param request:
    :return:
    """
    return HttpResponse(get_cached_data('key'))


def fetch_push_details(request, item_id):
    """

    :param request:
    :param item_id:
    :return: :raise:
    """
    try:
        return render_to_response('info/dpq_info_popup_contents.html',
                                  RequestContext(request, {'item': get_item_by_id(item_id)}))
    except KeyError:
        raise Http404(u'No parameters found in request.')


def fetch_queue_item(request):
    """

    :param request:
    :return: :raise:
    """
    try:
        data = loads(request.body)

        if data['mode'] == 'fetch':
            return render_to_response('modify/dpq_modify_popup_contents.html',
                                      RequestContext(request, {'item': get_item_by_id(data['id']),
                                                               'teams': get_teams(),
                                                               'active_branches': get_active_branches()}))
        elif data['mode'] == 'last':
            try:
                return render_to_response('add/dpq_add_popup_contents.html',
                                          RequestContext(request, {
                                              'item': QueueRecord.objects.filter(owner=request.user).order_by('-index')[
                                                  0],
                                              'teams': get_teams(),
                                              'active_branches': get_active_branches()}))
            except IndexError:
                return render_to_response('add/dpq_add_popup_contents.html',
                                          RequestContext(request, {'teams': get_teams(),
                                                                   'project_name': PROJECT_NAME,
                                                                   'active_branches': get_active_branches()}))
    except KeyError:
        raise Http404(u'No parameters found in request.')


@login_required
def create_queue_item(request):
    """

    :param request:
    :return: :raise:
    """
    try:
        data = loads(request.body)

        try:
            team = Team.objects.get(name__iexact=data['team'])
        except Team.DoesNotExist:
            team = None

        try:
            index = QueueRecord.objects.order_by('-index')[0].index + 1
        except IndexError:
            index = 1

        key_ = data['key']
        p = re.compile(PROJECT_NAME + "-{1,4}[0-9]")
        if not p.match(key_):
            key_ = PROJECT_NAME+"-0000"

        story = UserStory(
            key=key_,
            summary=data['summary'],
            assignee=data['developer'],
            tester=data['tester'],
            last_sync=None
        )

        # Panda Easter Egg (^_^)
        if story.tester.lower() == "panda":
            story.tester = story.assignee
            story.assignee = "I am Panda!!1"

        story.save()

        queue_record = QueueRecord(
            owner=request.user,
            queue_id=uuid1().hex,
            index=index,
            branch=Branch.objects.get(name__iexact=data['branch']),
            team=team,
            story=story
        )
        queue_record.save()
        invalidate_cache()
        update_key()
        return HttpResponse("OK")

    except KeyError:
        raise Http404(u'Illegal or missing parameters in create request.')


@login_required
def modify_queue_item(request):
    """

    :param request:
    :return: :raise:
    """
    try:
        data = loads(request.body)
        item = QueueRecord.objects.get(queue_id=data['id'])
        story = item.story

        key_ = data['key']
        p = re.compile(PROJECT_NAME + "-{1,4}[0-9]")
        if not p.match(key_):
            key_ = PROJECT_NAME+"-0000"

        story.key = key_
        story.summary = data['summary']
        story.assignee = data['developer']
        story.tester = data['tester']

        story.save()

        item.branch = Branch.objects.get(name__iexact=data['branch'])

        if data['team'] == 'none':
            item.team = None
        else:
            item.team = Team.objects.get(name__iexact=data['team'])

        item.modified_date = datetime.now()

        status_ = data['status']
        item.status = status_

        if status_ == QueueRecord.DONE or status_ == QueueRecord.REVERTED:
            item.done_date = datetime.now()
            update_daily_statistics(item.push_duration())

        if status_ == QueueRecord.SKIPPED:
            item.done_date = datetime.now()

        if status_ == QueueRecord.IN_PROGRESS or status_ == QueueRecord.JOKER_MODE:
            item.push_date = datetime.now()

        item.save()

        invalidate_cache()
        update_key()

        return HttpResponse('OK')

    except KeyError:
        raise Http404(u'Illegal or missing parameters in modify request.')


def history(request, branch):
    """

    :param request:
    :param branch:
    :return:
    """
    branch_obj = Branch.objects.get(name=branch)
    items_list = QueueRecord.objects.filter(branch=branch_obj, hidden=False,
                                            status__in=[QueueRecord.DONE, QueueRecord.REVERTED,
                                                        QueueRecord.SKIPPED]).order_by(
        '-done_date')

    for item in items_list:
        item.formatted_duration = str(timedelta(minutes=int(item.push_duration())))

    paginator = DiggPaginator(items_list, 15, body=5, padding=1, margin=2)

    current_page = request.GET.get('page')

    try:
        page = paginator.page(current_page)
    except (TypeError, PageNotAnInteger):
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render_to_response('history/dpq_history.html',
                              RequestContext(request, {'page': page,
                                                       'branch': branch_obj,
                                                       'jira_browse_url': JIRA_BROWSE_URL,
                                                       'active_branches': get_active_branches()}))


def help_page(request):
    """

    :param request:
    :return:
    """
    return render_to_response('dpq_help.html', RequestContext(request, {'active_branches': get_active_branches()}))


def logout_page(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect('/', RequestContext(request, {}))


def visualisation_average(request):
    """

    :param request:
    :return:
    """
    days = Statistics.objects.all().order_by('date')
    if days.count() > 14:
        days = days[days.count() - 14:]

    response = [['Date', 'Duration']]

    for day in days:
        average = day.total_push_duration / day.number_of_pushes
        response.append([day.date.strftime('%d.%m'), average])

    return HttpResponse(dumps(response))


def visualisation_branch_duration(request, branch, mode):
    """

    :param request:
    :param branch:
    :param mode:
    :return:
    """
    branch = Branch.objects.get(name=branch)
    last_pushes = QueueRecord.objects.filter(status__in=[QueueRecord.DONE, QueueRecord.REVERTED]).filter(
        branch=branch).order_by('index')
    if last_pushes.count() > 5:
        last_pushes = last_pushes[last_pushes.count() - 5:]

    response = [['Developer', 'Time']]
    for push in last_pushes:
        if push.push_date is not None and push.done_date is not None:
            if mode == 'duration':
                duration_obj = push.done_date - push.push_date
            if mode == 'pending':
                duration_obj = push.push_date - push.creation_date
            duration = int(duration_obj.total_seconds() / 60.0)
        else:
            duration = 0
        response.append([push.story.assignee, duration])

    if len(response) == 1:
        response.append(['no data available yet', 0])

    return HttpResponse(dumps(response))


def charts(request):
    """

    :param request:
    :return:
    """
    return render_to_response('dpq_charts.html', RequestContext(request, {'active_branches': get_active_branches()}))


@staff_member_required
def invalidate_application_cache(request):
    """

    :param request:
    :return:
    """
    invalidate_cache()
    return HttpResponse('Caches were invalidated.')


def register_page(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_password = form.cleaned_data['password1']
            User.objects.create_user(
                username=form_username,
                password=form_password,
            )
            CustomUserRecord.objects.create(
                django_user=User.objects.get(username__iexact=form_username),
                role=Role.objects.get(description__iexact='default'),
            )
            return redirect('/login/', RequestContext(request, {}))
            #return redirect('/maintenance/', RequestContext(request, {}))
    else:
        form = RegistrationForm()
    return render_to_response('registration/register.html', RequestContext(request, {'form': form}))


def fetch_superusers_list(request):
    """

    :param request:
    :return:
    """
    superusers_list = User.objects.filter(is_superuser=True)
    if superusers_list.exists():
        return render_to_response('dpq_superusers_list.html',
                                  RequestContext(request, {'superusers_list': superusers_list}))
    else:
        return HttpResponse("<center>List is empty.</center>")


@login_required
def move_queue_item(request):
    """

    :param request:
    :return: :raise:
    """
    try:
        data = loads(request.body)
        item = QueueRecord.objects.get(queue_id=data['id'])
        target = item
        index = item.index
        branch = item.branch

        if data['mode'] == 'down':
            target = QueueRecord.objects.filter(index__gt=index, branch=branch,
                                                status__in=[QueueRecord.WAITING, QueueRecord.IN_PROGRESS]).order_by(
                'index')[0]
        elif data['mode'] == 'up' and request.user.is_superuser:
            target = QueueRecord.objects.filter(index__lt=index, branch=branch,
                                                status__in=[QueueRecord.WAITING, QueueRecord.IN_PROGRESS]).order_by(
                '-index')[0]
        else:
            HttpResponse('Unknown mode')

        shift_indexes(item, target)

        return HttpResponse(item.index)
    except KeyError:
        raise Http404(u'Illegal or missing parameters in modify request.')


def search_page(request):
    return render_to_response('search/dpq_search.html',
                              RequestContext(request, {'active_branches': get_active_branches()}))


def search_results(request):
    data = loads(request.body)
    search_string = data['search_string']

    matching_stories = UserStory.objects.filter(Q(key__icontains=search_string) |
                                                Q(summary__icontains=search_string) |
                                                Q(assignee__icontains=search_string) |
                                                Q(tester__icontains=search_string))

    result = QueueRecord.objects.filter(story__in=matching_stories).order_by('-index')

    return render_to_response('search/dpq_search_results.html',
                              RequestContext(request, {'result': result,
                                                       'jira_browse_url': JIRA_BROWSE_URL}))


def heroes_and_villains(request):
    """

    :param request:
    :return:
    """
    try:
        hero_query = QueueRecord.objects.filter(
            status__iexact=QueueRecord.DONE).values('owner').annotate(item_count=Count('owner')).order_by(
            '-item_count')[0]
        hero = User.objects.get(id__iexact=hero_query['owner'])
        hero_count = hero_query['item_count']
    except IndexError:
        hero = None
        hero_count = 0

    try:
        skipper_query = QueueRecord.objects.filter(
            status__iexact=QueueRecord.SKIPPED).values('owner').annotate(item_count=Count('owner')).order_by(
            '-item_count')[0]
        skipper = User.objects.get(id__iexact=skipper_query['owner'])
        skipper_count = skipper_query['item_count']
    except IndexError:
        skipper = None
        skipper_count = 0

    try:
        reverter_query = QueueRecord.objects.filter(
            status__iexact=QueueRecord.REVERTED).values('owner').annotate(item_count=Count('owner')).order_by(
            '-item_count')[0]
        reverter = User.objects.get(id__iexact=reverter_query['owner'])
        reverter_count = reverter_query['item_count']
    except IndexError:
        reverter = None
        reverter_count = 0

    try:
        unhurried = QueueRecord.objects.get(
            queue_id=get_slowest_push_id(QueueRecord.objects.filter(status__in=[QueueRecord.DONE])))
        unhurried_duration = str(timedelta(minutes=int(unhurried.push_duration())))
    except IndexError:
        unhurried = None
        unhurried_duration = None

    return render_to_response('heroes/dpq_heroes_popup_content.html',
                              RequestContext(request, {'hero': hero,
                                                       'hero_count': hero_count,
                                                       'reverter': reverter,
                                                       'reverter_count': reverter_count,
                                                       'skipper': skipper,
                                                       'skipper_count': skipper_count,
                                                       'unhurried': unhurried,
                                                       'unhurried_duration': unhurried_duration}))


def maintenance_page(request):
    return render_to_response('misc/maintenance.html',
                              RequestContext(request, {}))


def get_story_data_from_JIRA(request):
    data = loads(request.body)
    story_key = data['key']

    story = fetch_story(story_key)

    if not story.success:
        raise Http404(u'Error occurred while communicating with JIRA')

    result = {
        'key': story_key,
        'summary': story.summary,
        'assignee': story.assignee,
        'tester': story.tester,
        'epic': story.epic,
        'reporter': story.reporter,
        'sp': story.points
    }

    json_response = dumps(result)

    return HttpResponse(json_response, mimetype='application/json')


@csrf_exempt
def api_update_branch_status(request):
    data = loads(request.body)
    try:
        branch_name = data['branch']
        status = data['status']
    except KeyError:
        response = {
            'status': 'error',
            'reason': 'missing parameter(s) in request'
        }
    if branch_name and status:
        try:
            branch = Branch.objects.get(name__iexact=branch_name)
            if branch:
                branch, response = change_branch_status(branch, status)
            else:
                response = {
                    'status': 'error',
                    'reason': 'incorrect status value, must be one of [success, failure]'
                }
        except ObjectDoesNotExist:
            response = {
                'status': 'error',
                'reason': 'branch does not exist'
            }
    return HttpResponse(dumps(response), mimetype='application/json')


def api_get_branches_statuses(request):
    response = []
    for branch in get_active_branches():
        response.append({
            "branch": branch.name,
            "status": branch.build_success
        })

    return HttpResponse(dumps(response), mimetype='application/json')


def kanban_cards(request):
    return render_to_response('dpq_kanban.html',
                              RequestContext(request, {'active_branches': get_active_branches()}))


def api_download_cards(request):
    story_keys = request.POST.get('print-data')
    if story_keys is None:
        response = {
                'status': 'error',
                'reason': 'invalid request'
            }
        return HttpResponse(dumps(response), mimetype='application/json')

    story_keys = story_keys.split(",")
    keys = filter(None, story_keys)

    cards = get_stories_from_list(keys)
    filename = render_cards(cards)

    return redirect('/media/cards/'+filename)


@login_required
def api_joker(request):
    try:
        data = loads(request.body)
        queue_id = data['id']
        queue_record = QueueRecord.objects.get(queue_id=queue_id)
        owner = queue_record.owner

        custom_user_record = CustomUserRecord.objects.get(django_user__id=owner.id)
        trump_cards_count = custom_user_record.trump_cards
        custom_user_record.trump_cards = trump_cards_count - 1
        custom_user_record.save()

        queue_record.status = QueueRecord.JOKER_MODE
        queue_record.save()

        invalidate_cache()

        response = {
            'status': 'success'
        }

    except KeyError:
        response = {
            'status': 'error',
            'reason': 'invalid request'
        }
    return HttpResponse(dumps(response), mimetype='application/json')


def retro_boards_list(request):
    boards_list = RetroBoard.objects.all().order_by('-creation_date')
    paginator = DiggPaginator(boards_list, 15, body=5, padding=1, margin=2)
    current_page = request.GET.get('page')
    try:
        page = paginator.page(current_page)
    except (TypeError, PageNotAnInteger):
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render_to_response('retro/dpq_retro.html', RequestContext(request, {'page': page,
                                                                               'active_branches': get_active_branches()}))


def retro_boards_sprint(request, sprint, team):
    sprint = Sprint.objects.get(number=sprint)
    team = Team.objects.get(name=team)
    is_active = RetroBoard.objects.get(sprint=sprint, team=team).is_active
    return render_to_response('retro/dpq_retro_sprintboard.html',
                              RequestContext(request, {'sprint': sprint.number,
                                                       'team': team,
                                                       'is_active': is_active,
                                                       'active_branches': get_active_branches()}))


def retro_board_table_contents(request, sprint, team):
    sprint = Sprint.objects.get(number=sprint)
    team = Team.objects.get(name=team)
    retro_board = RetroBoard.objects.get(sprint=sprint, team=team)

    stickers_good = BoardSticker.objects.filter(retroBoard=retro_board, type=BoardSticker.GOOD).order_by('-votes')
    stickers_good_with_voters = add_voters_list_to_stickers(stickers_good)

    stickers_change = BoardSticker.objects.filter(retroBoard=retro_board, type=BoardSticker.CHANGE).order_by('-votes')
    stickers_change_with_voters = add_voters_list_to_stickers(stickers_change)

    stickers_actions = BoardSticker.objects.filter(retroBoard=retro_board, type=BoardSticker.ACTION).order_by('-votes')
    return render_to_response('retro/dpq_retro_sprintboard_tables.html',
                              RequestContext(request, {'sprint': sprint.number,
                                                       'team': team,
                                                       'stickers_good': stickers_good_with_voters,
                                                       'stickers_change': stickers_change_with_voters,
                                                       'stickers_actions': stickers_actions}))


@login_required
def retro_board_add_sticker(request):
    try:
        data = loads(request.body)
        summary = data['summary']
        team = data['team']
        sprint = data['sprint']
        sticker_type = data['type']

        sprint = Sprint.objects.get(number=sprint)
        team = Team.objects.get(name=team)
        retro_board = RetroBoard.objects.get(sprint=sprint, team=team)
        creator = CustomUserRecord.objects.get(django_user=request.user)

        sticker = BoardSticker(
            created_by=creator,
            retroBoard=retro_board,
            summary=summary,
            type=sticker_type
        )
        sticker.save()
        response = {
            'status': 'OK'
        }
    except ObjectDoesNotExist:
        response = {
            'status': 'error',
            'reason': 'sprint or team does not exist'
        }
    except KeyError:
        response = {
            'status': 'error',
            'reason': 'illegal or missing parameters in request'
        }
    except ValueError:
        response = {
            'status': 'error',
            'reason': 'no JSON object could be decoded'
        }
    return HttpResponse(dumps(response), mimetype='application/json')


@login_required
def retro_board_voteup_sticker(request):
    try:
        data = loads(request.body)
        sticker_id = data['id']

        sticker = BoardSticker.objects.get(id=sticker_id)
        sticker.votes += 1

        voters = sticker.voters
        current_user_id = request.user.id

        if voters is not None:
            voters_list = voters.split(";")
            voters_list.append(unicode(current_user_id))
            voters_set = set(voters_list)
            sticker.voters = ";".join(str(x) for x in voters_set)
        else:
            sticker.voters = str(current_user_id)

        sticker.save()

        response = {
            'status': 'OK'
        }
    except ObjectDoesNotExist:
        response = {
            'status': 'error',
            'reason': 'sticker not found'
        }
    except ValueError:
        response = {
            'status': 'error',
            'reason': 'no JSON object could be decoded'
        }
    except KeyError:
        response = {
            'status': 'error',
            'reason': 'illegal or missing parameters in request'
        }
    return HttpResponse(dumps(response), mimetype='application/json')


@login_required
def retro_board_fetch_sticker(request):
    try:
        data = loads(request.body)
        sticker_id = data['id']

        sticker = BoardSticker.objects.get(id=sticker_id)

        return render_to_response('retro/popups/dpq_retro_modify_popup_content.html',
                                  RequestContext(request, {'sticker': sticker}))
    except ObjectDoesNotExist:
        response = {
            'status': 'error',
            'reason': 'sticker not found'
        }
    except ValueError:
        response = {
            'status': 'error',
            'reason': 'no JSON object could be decoded'
        }
    except KeyError:
        response = {
            'status': 'error',
            'reason': 'illegal or missing parameters in request'
        }
    return HttpResponse(dumps(response), mimetype='application/json')


@login_required
def retro_board_modify_sticker(request):
    try:
        data = loads(request.body)
        sticker_id = data['sticker_id']
        summary = data['summary']
        sticker_type = data['type']

        sticker = BoardSticker.objects.get(id=sticker_id)

        sticker.summary = summary
        sticker.type = sticker_type
        sticker.is_modified = 1
        sticker.modification_date = datetime.now()

        sticker.save()

        response = {
            'status': 'OK'
        }
    except ObjectDoesNotExist:
        response = {
            'status': 'error',
            'reason': 'sprint or team does not exist'
        }
    except KeyError:
        response = {
            'status': 'error',
            'reason': 'illegal or missing parameters in request'
        }
    except ValueError:
        response = {
            'status': 'error',
            'reason': 'no JSON object could be decoded'
        }
    return HttpResponse(dumps(response), mimetype='application/json')

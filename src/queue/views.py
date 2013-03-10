from datetime import datetime, date
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from exceptions import TypeError
from json import loads, dumps
from queue.forms import *
from queue.models import *
from queue.paginators import DiggPaginator
from queue.utils import *
from uuid import uuid1


def queue(request):
    try:
        current_tab = get_active_branches()[0].name
    except IndexError:
        raise Http404(u'No active branches.')
    return render_to_response('queue/dpq_queue.html',
        RequestContext(request, {'current_tab' : current_tab,
                                 'active_branches' : get_active_branches()}))
    

def refresh_branch(request, branch):
    return render_to_response('queue/dpq_queue_table_branch_tab.html',
        RequestContext(request, {'push_table' : get_last_pushes_for_branch(branch)}))


def request_key(request):
    return HttpResponse(get_cached_data('key'))


def fetch_push_details(request, item_id):
    try:
        return render_to_response('info/dpq_info_popup_contents.html',
                RequestContext(request, {'item' : get_item_by_id(item_id)}))
        
    except KeyError:
        raise Http404(u'No parameters found in request.')


def fetch_queue_item(request):
    try:
        data = loads(request.body)

        if(data['mode'] == 'fetch'):
            return render_to_response('modify/dpq_modify_popup_contents.html',
                RequestContext(request, {'item' : get_item_by_id(data['id']),
                                         'active_branches' : get_active_branches()}))

        elif(data['mode'] == 'last'):
            try:
                return render_to_response('add/dpq_add_popup_contents.html',
                    RequestContext(request, {'item' : Queue.objects.filter(owner=request.user).order_by('-index')[0],
                                             'active_branches' : get_active_branches()}))

            except IndexError:
                return render_to_response('add/dpq_add_popup_contents.html',
                    RequestContext(request, {'active_branches' : get_active_branches()}))

    except KeyError:
        raise Http404(u'No parameters found in request.')

@login_required
def create_queue_item(request):
    try:
        data = loads(request.body)

        try:
            index = Queue.objects.order_by('-index')[0].index + 1
        except IndexError:
            index = 1

        queue = Queue(
            ps=data['ps'],
            developerA=data['devA'],
            developerB=data['devB'],
            tester=data['tester'],
            description=data['description'],
            codereview_url=data['codereview_url'],
            branch=Branch.objects.get(name__iexact=data['branch']),
            owner=request.user,
            queue_id=uuid1().hex,
            index=index
        )
        queue.save()
        invalidate_cache()
        update_key()
        return HttpResponse("OK")

    except KeyError:
        raise Http404(u'Illegal or missing parameters in create request.')

@login_required
def modify_queue_item(request):
    try:
        data = loads(request.body)
        item = Queue.objects.get(queue_id=data["id"])

        item.ps = data['ps']
        item.developerA = data['devA']
        item.developerB = data['devB']
        item.tester = data['tester']

        item.branch = Branch.objects.get(name__iexact=data['branch'])

        item.description = data['description']
        item.codereview_url = data['codereview_url']
        item.status = data['status']

        item.modified_date = datetime.now()

        if(data['status'] == Queue.DONE or data['status'] == Queue.REVERTED):
            item.done_date = datetime.now()
            update_daily_statistics(item.push_duration())

        if(data['status'] == Queue.SKIPPED):
            item.done_date = datetime.now()

        if(data['status'] == Queue.IN_PROGRESS):
            item.push_date = datetime.now()

        old_index = int(item.index)
        new_index = int(data['index'])

        # Get index of the latest push in queue
        max_index = Queue.objects.order_by('-index')[0].index

        # Get all pushes with WAITING status
        waiting_items = Queue.objects.filter(status__iexact=Queue.WAITING).order_by('index')

        if(len(waiting_items) != 0):
            min_index = waiting_items[0].index
        else:
            min_index = max_index

        if(new_index > max_index):
            new_index = max_index

        if(new_index < min_index):
            new_index = min_index

        if((old_index != new_index) and
                (item.status == Queue.WAITING or
                 item.status == Queue.IN_PROGRESS)):

            item.index = 0
            item.save()

            if(new_index > old_index):
                for i in range(old_index + 1, new_index + 1):
                    try:
                        moving = Queue.objects.get(index__iexact=i)
                    except:
                        continue

                    moving.index = i - 1
                    moving.save()

            if(new_index < old_index):
                for i in range(old_index - 1, new_index - 1, -1):
                    try:
                        moving = Queue.objects.get(index__iexact=i)
                    except:
                        continue
                    moving.index = i + 1
                    moving.save()

            item.index = new_index
        item.save()
        invalidate_cache()
        update_key()

        return HttpResponse('OK')

    except KeyError:
        raise Http404(u'Illegal or missing parameters in modify request.')


def history(request, branch):
    branch_obj = Branch.objects.get(name=branch)
    list = Queue.objects.filter(branch=branch_obj, status__in=[Queue.DONE, Queue.REVERTED, Queue.SKIPPED]).order_by('-done_date')
    paginator = DiggPaginator(list, 15, body=5, padding=1, margin=2)

    current_page = request.GET.get('page')

    try:
        page = paginator.page(current_page)
    except (TypeError, PageNotAnInteger):
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render_to_response('history/dpq_history.html', 
                RequestContext(request, {'page' : page,
                                         'branch' : branch_obj,
                                         'active_branches' : get_active_branches()}))


def help_page(request):
    return render_to_response('dpq_help.html', RequestContext(request, {'active_branches' : get_active_branches()}))


def logout_page(request):
    logout(request)
    return redirect('/', RequestContext(request, {}))


def visualisation_average(request):
    days = Statistics.objects.all().order_by('date')
    if(days.count() > 14):
        days = days[days.count() - 14:]
        
    response = [['Date', 'Duration']]
    
    for day in days:
        average = day.total_push_duration / day.number_of_pushes
        response.append([day.date.strftime('%d.%m'), average])
    
    return HttpResponse(dumps(response))


def visualisation_branch_duration(request, branch, mode):
    branch = Branch.objects.get(name=branch)
    last_pushes = Queue.objects.filter(status__in=[Queue.DONE, Queue.REVERTED]).filter(branch=branch).order_by('index')
    if(last_pushes.count() > 5):
        last_pushes = last_pushes[last_pushes.count() - 5:]
    
    response = [['PS', 'Time']]
    for push in last_pushes:
        if(push.push_date != None and push.done_date != None):
            if(mode == 'duration'):
                duration_obj = push.done_date - push.push_date
            if(mode == 'pending'):
                duration_obj = push.push_date - push.creation_date
            duration = int(duration_obj.total_seconds() / 60.0)
        else:
            duration = 0 
        response.append([push.ps, duration])
    
    return HttpResponse(dumps(response))


def charts(request):
    return render_to_response('dpq_charts.html', RequestContext(request, {'active_branches' : get_active_branches()}))


@staff_member_required
def invalidate_application_cache(request):
    invalidate_cache()
    return HttpResponse('Caches were invalidated.')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            return redirect('/login/', RequestContext(request, {}))
    else:
        form = RegistrationForm()
    return render_to_response('registration/register.html', RequestContext(request, {'form': form}))


def fetch_superusers_list(request):
    superusers_list = User.objects.filter(is_superuser=True)
    if superusers_list.exists():
        return render_to_response('dpq_superusers_list.html', RequestContext(request, {'superusers_list': superusers_list}))
    else:
        return HttpResponse("<center>List is empty.</center>")

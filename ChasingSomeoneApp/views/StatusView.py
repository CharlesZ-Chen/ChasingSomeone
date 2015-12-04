__author__ = 'charleszhuochen'

import json
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse


from ChasingSomeoneApp.views import TwStatusView
from ChasingSomeoneApp.views import QrStatusView
from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.models.TwAccount import TwAccount
from ChasingSomeoneApp.models.QrAccount import QrAccount

# { 'site_type' : site_type }
@login_required
def refresh_status_by_site(request):
    if request.is_ajax():
        json_data = json.loads(request.body)
        try:
            site_type = json_data['site_type']
        except KeyError:
            return HttpResponse(False)
        user = request.user
        flr_list = Follower.objects.filter(user=user)
        if site_type == 'twitter':
            act_list = []
            since_id = json_data.get('since_id', None)
            for flr in flr_list:
                try:
                    act_list.append(TwAccount.objects.get(follower=flr))
                except TwAccount.DoesNotExist:
                    pass
            status_list = TwStatusView.refresh_status(act_list, since_id)
            return JsonResponse({'status_list': status_list})
        elif site_type == 'quora':
            act_list = []
            for flr in flr_list:
                try:
                    act_list.append(QrAccount.objects.get(follower=flr))
                except QrAccount.DoesNotExist:
                    pass
            status_list = QrStatusView.refresh_status(act_list)
            return JsonResponse({'status_list': status_list})
    raise Http404


# { 'flr_name': flr_name }
@login_required
def refresh_status_by_flr(request):
    if request.is_ajax():
        json_data = json.loads(request.body)
        try:
            flr_name = json_data['flr_name']
        except KeyError:
            return HttpResponse(False)
        lt_st_time = json_data.get('lt_st_time', None)
        status_list = []
        try:
            tw_account = TwAccount.objects.get(follower__name=flr_name)
            status_list.extend(TwStatusView.refresh_status([tw_account, ]))
        except TwAccount.DoesNotExist:
            pass
        try:
            qr_account = QrAccount.objects.get(follower__name=flr_name)
            status_list.extend(QrStatusView.refresh_status([qr_account, ]))
        except QrAccount.DoesNotExist:
            pass
        sorted_status_list = sorted(status_list, key=lambda status: status['time_stamp'], reverse=True)
        if lt_st_time:
            raw_struct_time = time.strptime(lt_st_time, '%Y-%m-%d %H:%M:%S')
            lt_st_time_epoch = time.mktime(raw_struct_time)
            sorted_status_list = filter(time_filter_wrapper(lt_st_time_epoch), sorted_status_list)
        elif len(sorted_status_list) > 10:
            sorted_status_list = sorted_status_list[:10]

        # sorted_status_list = sorted(status_list, key=lambda tw_status: tw_status['id'], cmp=status_cmp)
        return JsonResponse({'status_list': sorted_status_list})
    raise Http404


@login_required
def more_status_by_site(request):
    pass


@login_required
def more_status_by_flr(request):
    pass


def time_filter_wrapper(lt_st_time_epoch):
    def time_filter(status):
        raw_struct_time = time.strptime(status['time_stamp'], '%Y-%m-%d %H:%M:%S')
        time_epoch = time.mktime(raw_struct_time)
        return time_epoch > lt_st_time_epoch
    return time_filter

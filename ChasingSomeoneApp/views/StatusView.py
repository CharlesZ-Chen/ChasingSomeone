__author__ = 'charleszhuochen'

import json

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
    pass


@login_required
def more_status_by_site(request):
    pass


@login_required
def more_status_by_flr(request):
    pass

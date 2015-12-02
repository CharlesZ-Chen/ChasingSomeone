__author__ = 'charleszhuochen'

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse

from ChasingSomeoneApp.models.Follower import Follower
from ChasingSomeoneApp.views import AccountView


@login_required
def add_follower(request):
    if request.is_ajax():
        if request.method != 'POST':
            raise Http404
        json_data = json.loads(request.body)
        try:
            flr_name = json_data.get(u'flr_name')
        except KeyError:
            print("KeyError in FollowerView:add_follower() when getting flr_name\n")
            return HttpResponse(False)
        if Follower.objects.filter(name=flr_name).exists():
            return HttpResponse(False)
        new_follower = Follower(name=flr_name, user=request.user)
        new_follower.save()
        response_dict = {'flr_id': new_follower.id}
        return JsonResponse(response_dict)
    else:
        raise Http404


@login_required
def delete_follower(request):
    if request.is_ajax():
        if request.method != 'POST':
            raise Http404
        json_data = json.loads(request.body)
        try:
            flr_name = json_data.get(u'flr_name')
        except KeyError:
            print("KeyError in FollowerView:delete_follower() when getting flr_name\n")
            return HttpResponse(False)
        # act_list = AccountView.get_flr_accounts(flr_name)
        # for act in act_list:
        #     if not AccountView.delete_account(flr_name, act.get('act_type', None)):
        #         print("Error: delete_account return False when delete flr_name '%s', act_type '%s'"
        #               % (flr_name, act.get('act_type', None)))
        try:
            follower = Follower.objects.get(name=flr_name)
        except Follower.DoesNotExist:
            print("Error: FollowerView:delete_follower(): follower %s does not exist" % flr_name)
            return HttpResponse(False)
        follower.delete()
        return HttpResponse(True)
    raise Http404

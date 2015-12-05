__author__ = 'charleszhuochen'

'''AccountView is an inside View for controlling social accounts detials. it is like a controller of accounts'''
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse

from ChasingSomeoneApp.views import  TWAccountView, QrAccountView

from ChasingSomeoneApp.models.Follower import Follower

act_type_list = ['twitter', ]

# act_type, act_details
@login_required
def http_verify_account(request):
    if request.is_ajax():
        json_data = json.loads(request.body)
        if 'act_type' not in json_data:
            return HttpResponse(False)
        verify_result = verify_account(**json_data)
        if verify_result == False or verify_result == '404':
            return HttpResponse(verify_result)
        return JsonResponse(verify_result)
    raise Http404


@login_required
def http_save_account(request):
    if request.is_ajax():
        json_data = json.loads(request.body)
        if 'act_type' not in json_data:
            return HttpResponse(False)
        try:
            flr_name = json_data.get('flr_name')
        except KeyError:
            print("keyError in AccountView:http_save_account\n")
            return HttpResponse(False)
        try:
            follower = Follower.objects.get(name=flr_name)
        except Follower.DoesNotExist:
            print("cannot find follower with flr_name %s\n" % flr_name)
            return HttpResponse(False)

        save_result = save_account(follower, **json_data)
        return HttpResponse(save_result)
    raise Http404


@login_required
def http_delete_account(request):
    if request.is_ajax():
        json_data = json.loads(request.body)
        if 'act_type' not in json_data or 'flr_name' not in json_data:
            return HttpResponse(False)
        delete_result = delete_account(json_data.get('flr_name'), json_data.get('act_type'))
        return HttpResponse(delete_result)
    raise Http404


# follower:Follower, act_tpye, act_details
# tw_account needs details from crawler
def save_account(follower, **kwargs):
    if 'act_type' not in kwargs:
        return False
    verify_result = verify_account(**kwargs)
    if verify_result == '404' or verify_result is False:
        return verify_result
    kwargs.update(verify_result)
    try:
        act_type = kwargs['act_type']
    except KeyError:
        return False
    if act_type == u'twitter':
        act_kwargs = dict()
        try:
            act_kwargs['act_id'] = kwargs.get('act_id')
            act_kwargs['screen_name'] = kwargs.get('screen_name')
        except KeyError:
            print("key error in AccountView:save_account() with act_type 'twitter'\n")
            return False

        return TWAccountView.save_account(follower, **act_kwargs)
    elif act_type == u'quora':
        act_kwargs = dict()
        try:
            act_kwargs['user_name'] = kwargs['user_name']
        except KeyError:
            return False
        return QrAccountView.save_account(follower, **act_kwargs)
    return False


def verify_account(**kwargs):
    verify_result = False
    if kwargs.get(u'act_type', None) == u'twitter':
        try:
            verify_kwargs = {'flr_name': kwargs.get('flr_name', None),
                             'act_id': kwargs.get('act_id', None),
                             'screen_name': kwargs.get('screen_name', None)}
        except KeyError:
            print("key error when assign verify_kwargs in twitter\n")
            return False
        verify_result = TWAccountView.verify_account(**verify_kwargs)

    elif kwargs.get(u'act_type', None) == u'quora':

        verify_kwargs = {'flr_name': kwargs.get('flr_name', None),
                         'user_name': kwargs.get('user_name', None)}
        verify_result = QrAccountView.verify_account(**verify_kwargs)
    else:
        pass
    return verify_result


def delete_account(flr_name, act_type):
    if not Follower.objects.filter(name=flr_name).exists():
        return False
    if act_type == u'twitter':
        delete_result = TWAccountView.delete_account(flr_name)
        return delete_result
    elif act_type == u'quora':
        delete_result = QrAccountView.delete_account(flr_name)
        return delete_result
    else:
        # new act type add here
        pass
    return False


def get_flr_accounts(flr_name):
    act_list = []
    for act_type in act_type_list:
        act = get_account(flr_name, act_type)
        if act:
            act_list.append(act)
    return act_list


def get_account(flr_name, act_type):
    if act_type == u'twitter':
        act = TWAccountView.get_account(flr_name)
        if act:
            act['act_type'] = u'twitter'
        return act
    elif act_type == u'quora':
        act = QrAccountView.get_account(flr_name)
        if act:
            act['act_type'] = u'quora'
        return act
    else:
        pass
    return False

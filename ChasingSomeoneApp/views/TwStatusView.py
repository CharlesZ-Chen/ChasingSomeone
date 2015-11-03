__author__ = 'charleszhuochen'
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render

from ChasingSomeoneApp.models.TwStatus import TwStatus
from ChasingSomeoneApp.models.TwFollower import TwFollower
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter
import time
import json

def cmp(x, y):
    if x < y:
        return 1
    elif x == y:
        return 0
    return -1

@login_required
def get_status(request):
    if not request.method == 'POST':
        raise Http404
    pg_sts_count = 10
    user_id = request.user.id
    tw_follower_list = list(TwFollower.objects.filter(user_id=user_id))
    tw_crawler = Crawler_twitter()
    total_json_status_list = []
    json_status_list = []

    if 'id_latest_status' in request.POST:
        id_latest_status = request.POST['id_latest_status']
        for follower in tw_follower_list:
            json_status_list = tw_crawler.get_status(id=follower.follower_id, screen_name=follower.screen_name,
                                                     since_id=id_latest_status)
            total_json_status_list.extend(json_status_list)
    else:
        for follower in tw_follower_list:
            json_status_list = tw_crawler.get_status(id=follower.follower_id, screen_name=follower.screen_name)
            total_json_status_list.extend(json_status_list)

    if len(total_json_status_list) == 0:
        return HttpResponse(False)

    sorted_json_status_list = sorted(total_json_status_list, key=lambda tw_status: tw_status['id'],
                                         cmp=cmp)
    for json_status in sorted_json_status_list:
        if not TwStatus.objects.filter(pk=json_status['id_str']):
            status = TwStatus()
            status.id = json_status['id_str']
            for follower in tw_follower_list:
                if follower.screen_name == json_status['user']['screen_name']:
                    status.twFollower = follower
                    break
            status.text = json_status['text']
            transfer_ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(json_status['created_at'],
                                                                               '%a %b %d %H:%M:%S +0000 %Y'))
            status.created_at = transfer_ts
            status.save()
    if len(sorted_json_status_list) > 10:
        sorted_json_status_list = sorted_json_status_list[:10]
    transfer_json_status_list = []
    for json_status in sorted_json_status_list:
        status = transfer_json_status(json_status)
        transfer_json_status_list.append(status)
        dumped_json_status_list = json.dumps(transfer_json_status_list)
    return HttpResponse(dumped_json_status_list)


def transfer_json_status(json_status):
    text = None
    created_at = None
    lang = 'en'
    user = None
    profile_image_url_https = None
    screen_name = None
    user_id_str = None
    id_str = None
    if 'id' in json_status:
        id_str = json_status['id_str']
    if 'text' in json_status:
        text = json_status['text']
    if 'created_at' in json_status:
        created_at = json_status['created_at']
    if 'lang' in json_status:
        lang = json_status['lang']
    if 'user' in json_status:
        if 'profile_image_url_https' in json_status['user']:
            profile_image_url_https = json_status['user']['profile_image_url_https']
        if 'screen_name' in json_status['user']:
            screen_name = json_status['user']['screen_name']
        if 'id_str' in json_status['user']:
            user_id_str = json_status['user']['id_str']
    if 'user' in json_status:
        user = {u'profile_image_url_https': profile_image_url_https,
                u'screen_name': screen_name,
                u'user_id_str': user_id_str}
    status_aft_transfer = {u'text': text,
                           u'id': id_str,
                           u'created_at': created_at,
                           u'lang': lang,
                           u'user': user}
    return status_aft_transfer

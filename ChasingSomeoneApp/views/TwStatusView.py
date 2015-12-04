__author__ = 'charleszhuochen'

import time

from ChasingSomeoneApp.models.TwStatus import TwStatus
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter


def refresh_status(act_list, since_id=None):
    tw_crawler = Crawler_twitter()
    status_list = []
    for act in act_list:
        temp_list = tw_crawler.get_status(id=act.act_id, screen_name=act.screen_name, since_id=since_id)
        if temp_list:
            temp_list = transfer_status_list(temp_list)
            save_status(act, temp_list)
            status_list.extend(temp_list)

    if len(status_list) == 0:
        return []

    sorted_status_list = sorted(status_list, key=lambda tw_status: tw_status['id'], cmp=status_cmp)

    if len(sorted_status_list) > 10:
        sorted_status_list = sorted_status_list[:10]

    return sorted_status_list


def save_status(act, status_list):
    for status in status_list:
        if not TwStatus.objects.filter(pk=status['id']):
            new_status = TwStatus()
            new_status.id = status['id']
            new_status.twAccount = act
            new_status.text = status['text']
            new_status.created_at = status['created_at']
            new_status.save()


def more_status(act_id_list, max_id):
    pass


def transfer_status_list(json_status_list):
    status_list = []
    for json_status in json_status_list:
        status = transfer_json_status(json_status)
        status_list.append(status)
    return status_list


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
        raw_struct_time = time.strptime(json_status['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        time_epoch = time.mktime(raw_struct_time)
        time_epoch -= 8*3600
        offset_struct_time = time.localtime(time_epoch)
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', offset_struct_time)
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


def status_cmp(x, y):
    if x < y:
        return 1
    elif x == y:
        return 0
    return -1

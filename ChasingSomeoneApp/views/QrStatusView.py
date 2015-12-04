__author__ = 'charleszhuochen'

from ChasingSomeoneApp.models.QrStatus import QrStatus
from ChasingSomeoneApp.crawler.crawler_quora import Crawler_quora


def refresh_status(qr_act_list):
    qr_crawler = Crawler_quora()
    status_list = []
    for act in qr_act_list:
        temp_list = qr_crawler.get_status(user_name=act.user_name)
        if temp_list:
            save_status(act, temp_list)
            status_list.extend(temp_list)
    if len(status_list) > 10:
        status_list = status_list[:10]
    for status in status_list:
        status['act_type'] = 'quora'
    return status_list

def more_status(qr_act_list):
    pass

#current just use target as unique index
def save_status(act, status_list):
    for status in status_list:
        if not QrStatus.objects.filter(target=status.get('target', None)):
            new_status = QrStatus()
            new_status.qrAccount = act
            try:
                new_status.target = status['target']
                new_status.url_profile_img = status['user_profile_image']
                new_status.url_target = status['url']
                new_status.action_type = status['action_type']
                new_status.time_stamp = status['time_stamp']
                new_status.user_profile_name = status['user_name']
            except KeyError:
                continue
            new_status.save()

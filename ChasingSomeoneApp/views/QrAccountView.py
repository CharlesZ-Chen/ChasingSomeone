__author__ = 'charleszhuochen'

from ChasingSomeoneApp.crawler.crawler_quora import Crawler_quora
from ChasingSomeoneApp.models.QrAccount import QrAccount


def verify_account(**verify_kwargs):
    if verify_kwargs['flr_name'] is not None:
        if QrAccount.objects.filter(follower__name=verify_kwargs['flr_name']).exists():
            return False
    tw_crawler = Crawler_quora()
    crawler_kwargs = {'user_name': verify_kwargs.get('user_name', None)}
    user_name = tw_crawler.add_follower(**crawler_kwargs)
    if not user_name:
        return '404'
    return {'user_name': user_name}


def save_account(follower, **kwargs):
    new_account = QrAccount(follower=follower)
    new_account.user_name = kwargs['user_name']
    new_account.save()
    return True


def delete_account(follower_name):
    account = QrAccount.objects.get(follower__name=follower_name)
    if account:
        account.delete()
        return True
    else:
        return False


def get_account(flr_name):
    try:
        account = QrAccount.objects.get(follower__name=flr_name)
        return {'user_name': account.user_name}
    except QrAccount.DoesNotExist:
        return False

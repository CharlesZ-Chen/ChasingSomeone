__author__ = 'charleszhuochen'

from django.http import HttpResponse, Http404
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter
from django.contrib.auth.decorators import login_required
from ChasingSomeoneApp.models import TwAccount


@login_required
def add_follower(request):
    if request.method == 'POST':
        tw_crawler = Crawler_twitter()
        follower_id = request.POST['follower_id']
        screen_name = request.POST['screen_name']

        kwargs = {'screen_name': screen_name,
                  'id': follower_id}
        is_exist_follower = tw_crawler.add_follower(**kwargs)
        if not is_exist_follower:
            return HttpResponse(False)
        else:
            if TwAccount.objects.filter(user_id=request.user.id).filter(follower_id=is_exist_follower['id']).exists():
                return HttpResponse(False)
            new_follower = TwAccount()
            new_follower.follower_id = is_exist_follower['id']
            new_follower.screen_name = is_exist_follower['screen_name']
            new_follower.user = request.user
            new_follower.save()
            return HttpResponse(True)
    else:
        raise Http404


def verify_account(**verify_kwargs):
    if verify_kwargs['flr_name'] is not None:
        if TwAccount.objects.filter(follower__name=verify_kwargs['flr_name']).exists():
            return False
    tw_crawler = Crawler_twitter()
    if verify_kwargs['act_id'] == u'None':
        verify_kwargs['act_id'] = None
    if verify_kwargs['screen_name'] == u'None':
        verify_kwargs['screen_name'] = None
    crawler_kwargs = {'id': verify_kwargs['act_id'],
                      'screen_name': verify_kwargs['screen_name']}
    is_exist_follower = tw_crawler.add_follower(**crawler_kwargs)
    if not is_exist_follower:
        return '404'
    # rename for consistency
    is_exist_follower['act_id'] = is_exist_follower.pop('id')
    return is_exist_follower


def save_account(follower, **kwargs):
    new_account = TwAccount(follower=follower)
    new_account.act_id = kwargs['act_id']
    new_account.screen_name = kwargs['screen_name']
    new_account.save()
    return True


def delete_account(follower_name):
    account = TwAccount.objects.get(follower__name=follower_name)
    if account:
        account.delete()
        return True
    else:
        return False


def get_account(flr_name):
    try:
        account = TwAccount.objects.get(follower__name=flr_name)
        return {'act_id': account.act_id, 'screen_name': account.screen_name}
    except TwAccount.DoesNotExist:
        return False

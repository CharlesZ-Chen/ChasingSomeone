__author__ = 'charleszhuochen'

from django.http import HttpResponse, Http404
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter
from django.contrib.auth.decorators import login_required
from ChasingSomeoneApp.models import TwFollower


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
            if TwFollower.objects.filter(user_id=request.user.id).filter(follower_id=is_exist_follower['id']).exists():
                return HttpResponse(False)
            new_follower = TwFollower()
            new_follower.follower_id = is_exist_follower['id']
            new_follower.screen_name = is_exist_follower['screen_name']
            new_follower.user = request.user
            new_follower.save()
            return HttpResponse(True)
    else:
        raise Http404

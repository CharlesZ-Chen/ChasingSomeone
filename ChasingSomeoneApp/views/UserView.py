__author__ = 'charleszhuochen'
from random import choice
from string import letters

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ChasingSomeoneApp.forms import SignUpForm, UserProfileForm
from ChasingSomeoneApp.models.UserProfile import User

# Create your views here.


def register(request):
    registered = False

    if request.method == 'POST':
        # random username
        data = request.POST.copy()
        data['username'] = ''.join([choice(letters) for i in xrange(30)])
        signup_form = SignUpForm(data=data)
        profile_form = UserProfileForm(data=request.POST)

        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()
            # user.set_password(user.password)
            # user.save()

            #associate profile with user
            profile = profile_form.save(commit=False)
            profile.user = user

            #File related attributes should assign here with if condition

            #save profile
            profile.save()
            subject = 'Activate Your Chasing Someone Account'
            msg = "please click the following link to activate your account:\n"
            user = User.objects.get(email=user.email)
            msg += "http://127.0.0.1:8000" + reverse('ChasingSomeoneApp:user_activate', kwargs={'user_pk': user.pk})
            send_mail(subject,
                      msg,
                      settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
            registered = True

        else:
            print signup_form.errors, profile_form.errors
    else:
        signup_form = SignUpForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form': signup_form,
                    'profile_form': profile_form,
                    'registered': registered}
    return render(request, 'ChasingSomeoneApp/register.html', context_dict)


def user_home(request):
    if request.user.is_authenticated():
        return render(request, 'ChasingSomeoneApp/user_home.html')
    else:
        return HttpResponseRedirect(reverse('ChasingSomeoneApp:user_login'))

def user_activate(request, user_pk):
    user = User.objects.get(pk=user_pk)
    activated = False
    if user:
        user.is_active = True
        user.save()
        activated = True
    context_dict = {'activated': activated}
    return render(request, 'ChasingSomeoneApp/user_active.html', context_dict)

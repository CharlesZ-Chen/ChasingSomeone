__author__ = 'charleszhuochen'

import json
from django.test import Client
from ChasingSomeoneApp.models.UserProfile import User


def set_up():
    user = User(username='testUser', email='testUser@test.com')
    user.set_password('123')
    user.is_active = True
    user.save()
    client = Client()
    client.login(username='testUser@test.com', password='123')
    client.get('/ChasingSomeone/home/')
    return {'client': client, 'user': user}


def ajax_post_json(client, post_url, ajax_dict):
    json_data = json.dumps(ajax_dict)
    response = client.post(post_url,  json_data, 'json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    return response

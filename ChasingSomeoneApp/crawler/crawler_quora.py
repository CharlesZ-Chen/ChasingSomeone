#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
crawler quora using the build-in library
add_follower(user_name=)
    return true or false
get_status(user_name=)
    return a list of dictionaries
'''

__author__ = 'Quan Zhang'

from bs4 import BeautifulSoup
import urllib2
import re
from datetime import datetime, timedelta

# http://api.quora.com/api/do_action_POST


class Crawler_quora(object):

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'
        self.headers = headers = {'User-Agent': self.user_agent}
        self.base_url = 'https://www.quora.com'
        self.page = None
        self.time_reg = re.compile(r'(\d+)([smhdw]).*')

    def get_page(self, user_name):
        url = self.base_url + '/profile/' + user_name
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            self.page = response.read().decode('utf-8')
            return True
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print 'Error occured when getting page, error num', e.code
                return False
            if hasattr(e, 'reason'):
                print 'Error occured when getting page, error num', e.reason
                return False

    def add_follower(self, *args, **kwargs):
        user_name = kwargs.get('user_name')
        if not user_name:
            return False
        if not self.get_page(user_name):
            return False
        soup = BeautifulSoup(self.page, 'html.parser')
        page_not_found = soup.select('div[class="message_body"]')
        # print page_not_found
        if page_not_found:
            text = page_not_found.get_text()
            if text == u'The page you were looking for could not be found.':
                print 'The page you were looking for could not be found.'
                return False
        # otherwise, page specified by user_name is found
        return user_name

    def get_standard_time(self, time_string):
        now_time = datetime.now()
        match_res = self.time_reg.match(time_string)
        if match_res:
            number = int(match_res.group(1))
            unit = match_res.group(2)
            # print number, unit
            if not number or not unit:
                return now_time.strftime('%Y-%m-%d %H:%M:%S')
            if unit == 'w':
                now_time = now_time - timedelta(weeks=number)
            elif unit == 's':
                now_time = now_time - timedelta(seconds=number)
            elif unit == 'm':
                now_time = now_time - timedelta(minutes=number)
            elif unit == 'h':
                now_time = now_time - timedelta(hours=number)
            elif unit == 'd':
                now_time = now_time - timedelta(days=number)
        return now_time.strftime('%Y-%m-%d %H:%M:%S')

    #  here to update event header
    def get_event_header(self, inner_item):
        if not inner_item:
            return None
        tmp_dict = {}
        action = inner_item.get_text()
        # print action
        if action:
            action_text = None
            if action.find('upvoted') != -1:
                action_text = 'upvoted'
            elif action.find('wrote') != -1:
                action_text = 'wrote'
            elif action.find('followed') != -1:
                action_text = 'followed'
            elif action.find('asked') != -1:
                action_text = 'asked'
            tmp_dict['action_type'] = action_text
        user = inner_item.find('a', class_='user')
        if user:
            tmp_dict['user_name'] = user.get_text()
        user_image = inner_item.find('img', class_='profile_photo_img')
        if user_image:
            tmp_dict['user_profile_image'] = user_image.get('src')
        time_stamp = inner_item.find('span', class_='timestamp')
        if time_stamp:
            tmp_dict['time_stamp'] = self.get_standard_time(time_stamp.get_text())
        return tmp_dict

    def extract_status(self, list_item):
        if not list_item:
            return {}
        status_dict = {}
        for item in list_item.children:
            # print item.prettify()
            # print item.get('id')
            # print item.get('class')
            item_class_name = item.get('class')
            if item_class_name:
                item_class_name = item_class_name[0]
            if not item_class_name:
                # for inner_item in item.children:
                class_name = item.find('div', class_='EventHeader')
                if class_name:
                    res = self.get_event_header(class_name)
                    if res:
                        status_dict.update(res)
                class_name = item.find('div', class_='QuestionText')
                if class_name:
                    target = class_name.find('span', class_='question_text').get_text()
                    link = class_name.find('a', class_='question_link').get('href')
                    if target:
                        status_dict['target'] = target
                    if link:
                        status_dict['url'] = (self.base_url + link)
            elif item_class_name == u'object_follow_story':
                info = item.find('a', class_='user')
                if info:
                    status_dict['target'] = info.get_text()
                    status_dict['url'] = self.base_url + info.get('href')
                    continue
                info = item.find('a', class_='TopicNameLink HoverMenu topic_name')
                if info:
                    status_dict['target'] = info.find('span', 'TopicNameSpan TopicName').get_text()
                    status_dict['url'] = self.base_url + info.get('href')
        return status_dict

    def get_status(self, *args, **kwargs):
        user_name = kwargs.get('user_name')
        limit = kwargs.get('limit')
        if not type or type(limit) != int or limit > 15 or limit < 1:
            limit = 10
        if not user_name:
            return []
        if not self.get_page(user_name):
            return []
        soup = BeautifulSoup(self.page, 'html.parser')
        list_item = soup.find_all('div', class_='feed_item_inner', limit=limit)
        # for item in list_item:
        #     print type(item), item
        if not list_item:
            return []
        result_list = []
        for item in list_item:
            result_dict = self.extract_status(item)
            if result_dict:
                result_list.append(result_dict)
        return result_list



if __name__ == '__main__':
    crawler = Crawler_quora()
    print crawler.add_follower(user_name='Dan-Holliday')
    print crawler.add_follower(user_name='colin-27')
    posts = crawler.get_status(user_name='Colin-Barrett')
    for update in posts:
        print update
    post = crawler.get_status(user_name='quan-zhang-27')
    for update in post:
        print update

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'unittest for class crawler quora'

__author__ = 'Quan Zhang'

import unittest
from ChasingSomeoneApp.crawler.crawler_quora import Crawler_quora

class CrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler_quora()

    def tearDown(self):
        self.crawler = None

    def test_add_follower(self):
        self.assertFalse(self.crawler.add_follower(),
                         'add follower with empty information')
        self.assertFalse(self.crawler.add_follower(id = '51248642'),
                         'add follower with wrong information')
        self.assertFalse(self.crawler.add_follower(user_name='wahahahah'),
                         'no such user')
        self.assertIsNotNone(self.crawler.add_follower(user_name='quan-zhang-27'),
                             'add follower with correct screen name')
        self.assertEqual(self.crawler.add_follower(user_name='quan-zhang-27'), 'quan-zhang-27',
                         'check return id if is equal to given correct id')

    def test_get_status(self):
        self.assertEqual(self.crawler.get_status(), [],
                         'get status with empty information')
        self.assertEqual(self.crawler.get_status(id = '51248642'), [],
                         'get status with incorret information')
        self.assertEqual(self.crawler.get_status(user_name='wahahahah'), [],
                         'get status with wrong user name')
        self.assertNotEqual(len(self.crawler.get_status(user_name='quan-zhang-27')), 0,
                         'get status with correct screen name')
        self.assertNotEqual(len(self.crawler.get_status(user_name='Dan-holliday')), 0,
                             'get status with correct user name')


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(CrawlerTestCase)
    # alltests = unittest.TestSuite([suite])
    # runner = unittest.TextTestRunner()
    # runner.run (alltests)
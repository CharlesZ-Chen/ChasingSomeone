#!/usr/bin/env python
# -*- coding: utf-8 -*-

'unittest for class crawler'

__author__ = 'Quan Zhang'

import unittest
from ChasingSomeoneApp.crawler.crawler_twitter import Crawler_twitter

class CrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler_twitter()

    def tearDown(self):
        self.crawler = None

    def test_add_follower(self):
        self.assertFalse(self.crawler.add_follower(),
                         'add follower with empty information')
        self.assertFalse(self.crawler.add_follower(id = '51248642'),
                         'add follower with wrong information')
        self.assertIsNotNone(self.crawler.add_follower(screen_name = 'matthewperryfan'),
                             'add follower with correct screen name')
        self.assertEqual(self.crawler.add_follower(id = '30653573').get('id'), '30653573',
                         'check return id if is equal to given correct id')

    def test_get_status(self):
        self.assertEqual(self.crawler.get_status(), [],
                         'get status with empty information')
        self.assertEqual(self.crawler.get_status(id = '51248642'), [],
                         'get status with incorret information')
        self.assertNotEqual(len(self.crawler.get_status(screen_name = 'matthewperryfan')), 0,
                         'get status with correct screen name')
        self.assertNotEqual(len(self.crawler.get_status(id = '30653573')), 0,
                             'get status with correct id')


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(CrawlerTestCase)
    # alltests = unittest.TestSuite([suite])
    # runner = unittest.TextTestRunner()
    # runner.run (alltests)
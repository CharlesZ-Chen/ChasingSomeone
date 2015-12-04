#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quan Zhang'

import time
import subprocess

while True:
    command = 'python /Users/ZhangQuan/Documents/courses/ECE651/ChasingSomeone/manage.py email_sender'
    subprocess.call(command, shell=True)
    time.sleep(60)
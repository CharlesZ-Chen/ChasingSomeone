#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quan Zhang'

import time
import subprocess

while True:
    command = 'python ./manage.py email_sender'
    subprocess.call(command, shell=True)
    time.sleep(15)
#!/usr/bin/env python

import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                os.pardir,os.pardir)))
from manager import Plugin, PluginManager

class CountHTTP200(Plugin):
    """
    This Class object counts HTTP 200 status codes
    """

    def __init__(self, **kwargs):
        self.keywords = ['counter']
        self.counter_200 = 0
        self.counter_total = 0

    def process(self, **kwargs):
        print kwargs
        print kwargs['status']
        if 'status' in kwargs:
            self.counter_total += 1
            if kwargs['status'] == '200':
                self.counter_200 += 1

    def report(self, **kwargs):
        print '== HTTP code 200 counter =='
        print "HTTP 200 responses: %d" % self.counter_200
        print "All responses: %d" % self.counter_total

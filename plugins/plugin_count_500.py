#!/usr/bin/env python

from manager import Plugin

class CountHTTP500(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter']
        self.counter_500 = 0
        self.counter_total = 0

    def process(self, **kwargs):
        if 'status' in kwargs:
            self.counter_total += 1
            if kwargs['status'] == '500':
                self.counter_500 += 1

    def report(self, **kwargs):
        print '== HTTP code 500 counter =='
        print "HTTP 500 responses: %d" % self.counter_500
        print "All responses: %d" % self.counter_total

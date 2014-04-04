#!/usr/bin/env python

from manager import Plugin

class CountHTTP404(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter']
        self.counter_404 = 0
        self.counter_total = 0

    def process(self, **kwargs): #
        if 'status' in kwargs:
            self.counter_total += 1
            if kwargs['status'] == '404':
                self.counter_404 += 1

    def report(self, **kwargs):
        print '== HTTP code 404 counter =='
        print "HTTP 404 responses: %d" % self.counter_404
        print "All responses: %d" % self.counter_total

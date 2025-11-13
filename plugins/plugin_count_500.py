#!/usr/bin/env python3

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
        print('== HTTP code 500 counter ==')
        print(f"HTTP 500 responses: {self.counter_500}")
        print(f"All responses: {self.counter_total}")

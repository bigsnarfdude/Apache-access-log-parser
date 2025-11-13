#!/usr/bin/env python3

from manager import Plugin

class CountHTTP200(Plugin):
    """
    This Class object counts HTTP 200 status codes
    """

    def __init__(self, **kwargs):
        self.keywords = ['counter']
        self.counter_200 = 0
        self.counter_total = 0

    def process(self, **kwargs):
        print(kwargs)
        print(kwargs['status'])
        if 'status' in kwargs:
            self.counter_total += 1
            if kwargs['status'] == '200':
                self.counter_200 += 1

    def report(self, **kwargs):
        print('== HTTP code 200 counter ==')
        print(f"HTTP 200 responses: {self.counter_200}")
        print(f"All responses: {self.counter_total}")

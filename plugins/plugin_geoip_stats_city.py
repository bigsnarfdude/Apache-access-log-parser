#!/usr/bin/env python
from manager import Plugin
from operator import itemgetter

import pygeoip

class GeoIPStats(Plugin):

    def __init__(self, **kwargs):
        self.gic = pygeoip.GeoIP('/Users/antigen/dev/Apache-access-log-parser/geo_data_files/GeoLiteCity.dat')
        self.cities = {}

    def process(self, **kwargs):
        if 'remote_host' in kwargs:
            city = self.gic.record_by_name(kwargs['remote_host'])['city']
            if city in self.cities:
                self.cities[city] += 1
            else:
                self.cities[city] = 1

    def report(self, **kwargs):
        print "== Requests by city =="
        for (city, count) in sorted(self.cities.iteritems(), key=itemgetter(1), reverse=True):
            print " %10d: %s" % (count, city)


#!/usr/bin/env python3
from manager import Plugin
from operator import itemgetter
import os

import pygeoip

class GeoIPStats(Plugin):

    def __init__(self, **kwargs):
        # Use relative path from project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        geoip_city_path = os.path.join(project_root, 'geo_data_files', 'GeoLiteCity.dat')

        if not os.path.exists(geoip_city_path):
            print(f"Warning: GeoIP City database not found at {geoip_city_path}")
            self.gic = None
        else:
            self.gic = pygeoip.GeoIP(geoip_city_path)
        self.cities = {}

    def process(self, **kwargs):
        if self.gic and 'remote_host' in kwargs:
            city = self.gic.record_by_name(kwargs['remote_host'])['city']
            if city in self.cities:
                self.cities[city] += 1
            else:
                self.cities[city] = 1

    def report(self, **kwargs):
        print("== Requests by city ==")
        for (city, count) in sorted(self.cities.items(), key=itemgetter(1), reverse=True):
            print(f" {count:>10d}: {city}")


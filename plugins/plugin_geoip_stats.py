#!/usr/bin/env python3
from manager import Plugin
from operator import itemgetter
import os

import pygeoip

class GeoIPStats(Plugin):

    def __init__(self, **kwargs):
        # Use relative path from project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        geoip_path = os.path.join(project_root, 'geo_data_files', 'GeoIP.dat')

        if not os.path.exists(geoip_path):
            print(f"Warning: GeoIP database not found at {geoip_path}")
            self.gi = None
        else:
            self.gi = pygeoip.GeoIP(geoip_path)
        self.countries = {}

    def process(self, **kwargs):
        if self.gi and 'remote_host' in kwargs:
            country = self.gi.country_name_by_addr(kwargs['remote_host'])
            if country in self.countries:
                self.countries[country] += 1
            else:
                self.countries[country] = 1

    def report(self, **kwargs):
        print("== Requests by country ==")
        for (country, count) in sorted(self.countries.items(), key=itemgetter(1), reverse=True):
            print(f" {count:>10d}: {country}")


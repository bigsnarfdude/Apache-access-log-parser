import unittest
import os
import sys
from plugins.plugin_count_404 import CountHTTP404
from plugins.plugin_count_200 import CountHTTP200
from manager import Plugin, PluginManager


class TestApacheLogParser(unittest.TestCase):

    def test_plugin_manager_loading_plugins(self):
        pass

    def test_plugin(self):
        # test the combined example from apache.org
        #self.combined_log_entry = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08 [en] (Win98; I ;Nav)"'
        simple = { 'status':'200' }
        plugin_manager = PluginManager()
        plugin_manager.call_method(method='process', args = simple)

        for item in plugin_manager.plugins:
            if isinstance(item, CountHTTP200):
                self.assertEquals (1, item.counter_total)
                self.assertEquals (1, item.counter_200)

    def test_404_plugin(self):

        simple = { 'status':'404' }
        plugin_manager = PluginManager()
        plugin_manager.call_method(method='process', args = simple)

        for item in plugin_manager.plugins:
            if isinstance(item, CountHTTP404):
                self.assertEquals(1, item.counter_total)
                self.assertEquals(1, item.counter_404)


"""
    def testCommonExample(self):
        # test the common example from apache.org
        common_log_entry = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '\
                           '"GET /apache_pb.gif HTTP/1.0" 200 2326' 
        self.assertEqual(apache_log_parser_split.dictify_logline(common_log_entry),
                        {'remote_host': '127.0.0.1', 'status': '200', 'bytes_sent': '2326'})
    
    def testExtraWhitespace(self):
        # test for extra whitespace between fields
        common_log_entry = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '\ 
                           '"GET /apache_pb.gif HTTP/1.0" 200 2326' 
        self.assertEqual(apache_log_parser_split.dictify_logline(common_log_entry),
                        {'remote_host': '127.0.0.1', 'status': '200', 'bytes_sent': '2326'})
            
    def testMalformed(self):
        # test for extra whitespace between fields
        common_log_entry = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] '\ 
                           '"GET /some/url/with white space.html HTTP/1.0" 200 2326' 
        self.assertEqual(apache_log_parser_split.dictify_logline(common_log_entry),
                        {'remote_host': '127.0.0.1', 'status': '200', 'bytes_sent': '2326'})

"""

if __name__ == '__main__': 
    unittest.main()

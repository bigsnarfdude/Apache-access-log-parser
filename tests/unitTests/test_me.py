
'''
Nose testing tutorial and learning

assert - base assert allowing you to write your own assertions
assertEqual(a, b) - check a and b are equal
assertNotEqual(a, b) - check a and b are not equal
assertIn(a, b) - check that a is in the item b
assertNotIn(a, b) - check that a is not in the item b
assertFalse(a) - check that the value of a is False
assertTrue(a) - check the value of a is True
assertIsInstance(a, TYPE) - check that a is of type "TYPE"
assertRaises(ERROR, a, args) - check that when a is called with args that it raises ERROR

'''

import unittest
from nose.tools import with_setup


def test_b():
    assert 'b' == 'b'


class TestStatus500:
    def test_c(self):
        assert 'c' == 'c'
    def test_500(self):
        pass


class ExampleTest(unittest.TestCase):
    def test_a(self):
        self.assert_(1 == 1)

def multiply(a,b):
    return a*b

class TestMultiply(unittest.TestCase):
    def test_numbers_3_4(self):
        assert multiply((3,4), 12)


##############################
# setup and teardown fixtures
##############################

class TestFooClass(unittest.TestCase):
   def setup_foo_value(self):
      self.foo = 'foobar'

   @with_setup(setup_foo_value)
   def test_something(self):
      print self.foo

##############################
# setup and teardown fixtures
##############################

def my_setup_function():
    pass
 
def my_teardown_function():
    pass
 
@with_setup(my_setup_function, my_teardown_function)
def test_numbers_3_4():
    assert multiply(3,4) == 12 
    
"""
full example dunno what it does
"""

def setup_module(module):
    print ("") # this is to get a newline after the dots
    print ("setup_module before anything in this file")
 
def teardown_module(module):
    print ("teardown_module after everything in this file")
 
def my_setup_function():
    print ("my_setup_function")
 
def my_teardown_function():
    print ("my_teardown_function")
 
@with_setup(my_setup_function, my_teardown_function)
def test_numbers_3_4():
    print 'test_numbers_3_4  <============================ actual test code'
    assert multiply(3,4) == 12
 
@with_setup(my_setup_function, my_teardown_function)
def test_strings_a_3():
    print 'test_strings_a_3  <============================ actual test code'
    assert multiply('a',3) == 'aaa'
 
 
class TestUM:
 
    def setup(self):
        print ("TestUM:setup() before each test method")
 
    def teardown(self):
        print ("TestUM:teardown() after each test method")
 
    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
 
    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")
 
    def test_numbers_5_6(self):
        print 'test_numbers_5_6()  <============================ actual test code'
        assert multiply(5,6) == 30
 
    def test_strings_b_2(self):
        print 'test_strings_b_2()  <============================ actual test code'
        assert multiply('b',2) == 'bb'
 

import unittest
from tornadorpc.utils import getcallargs

class TestCallArgs(unittest.TestCase):
    """ Tries various argument settings """

    def test_no_args(self):
        def test():
            pass
        kwargs, xtra = getcallargs(test)
        self.assertTrue(kwargs == {})
        self.assertTrue(xtra == [])
        
    def test_bad_no_args(self):
        def test():
            pass
        self.assertRaises(TypeError, getcallargs, test, 5)
        
    def test_positional_args(self):
        def test(a, b):
            pass
        kwargs, xtra = getcallargs(test, 5, 6)
        self.assertTrue(kwargs == {'a':5, 'b': 6})
        self.assertTrue(xtra == [])
        
    def test_extra_positional_args(self):
        def test(a, b, *args):
            pass
        kwargs, xtra = getcallargs(test, 5, 6, 7, 8)
        self.assertTrue(kwargs == {'a': 5, 'b': 6})
        self.assertTrue(xtra == [7, 8])
    
    def test_bad_positional_args(self):
        def test(a, b):
            pass
        self.assertRaises(TypeError, getcallargs, test, 5)
       
    def test_keyword_args(self):
        def test(a, b):
            pass
        kwargs, xtra = getcallargs(test, a=5, b=6)
        self.assertTrue(kwargs == {'a': 5, 'b':6})
        self.assertTrue(xtra == [])

    def test_extra_keyword_args(self):
        def test(a, b, **kwargs):
            pass
        kwargs, xtra = getcallargs(test, a=5, b=6, c=7, d=8)
        self.assertTrue(kwargs == {'a':5, 'b':6, 'c':7, 'd':8})
        self.assertTrue(xtra == [])
        
    def test_bad_keyword_args(self):
        def test(a, b):
            pass
        self.assertRaises(TypeError, getcallargs, test, a=1, b=2, c=5)
        
    def test_method(self):
        class Foo(object):
            def test(myself, a, b):
                pass
        foo = Foo()
        kwargs, xtra = getcallargs(foo.test, 5, 6)
        self.assertTrue(kwargs == {'a':5, 'b':6})
        self.assertTrue(xtra == [])
        
    def test_default(self):
        def test(a, b, default=None):
            pass
        kwargs, xtra = getcallargs(test, a=5, b=6)
        self.assertTrue(kwargs == {'a':5, 'b':6, 'default':None})
        self.assertTrue(xtra == [])

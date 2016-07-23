__author__ = 'sparky'
import unittest
import sys, os
print(sys.path)
if __name__ == '__main__':

#    sys.path.insert(0, os.path.dirname(__file__))
    suite = unittest.TestLoader().discover('.', pattern="test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite)

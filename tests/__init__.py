"""Runner for unittests"""
import unittest
from . import unit

def create_suite():
    """Create test suite for unittest"""
    suite = unittest.TestSuite()
    suite.addTest(unit.Test())
    suite.addTest(unit.TestLoad())
    # return configured testsuite
    return suite

if __name__ == "__main__":
    # run all
    unittest.TextTestRunner().run(create_suite())

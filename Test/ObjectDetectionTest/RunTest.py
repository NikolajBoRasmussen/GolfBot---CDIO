import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Test.ObjectDetectionTest.InitialTest import InitialTests
from Test.ObjectDetectionTest.test1 import Tests1
from Test.ObjectDetectionTest.test2 import Tests2
from Test.ObjectDetectionTest.test3 import Tests3


def run_all():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test_case in (InitialTests, Tests1, Tests2, Tests3):
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Failures: {len(result.failures)}, Errors: {len(result.errors)}")

run_all()

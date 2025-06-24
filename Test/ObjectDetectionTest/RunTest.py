import unittest
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Test.ObjectDetectionTest.InitialTest import InitialTests
from Test.ObjectDetectionTest.test1 import Tests1
from Test.ObjectDetectionTest.test2 import Tests2
from Test.ObjectDetectionTest.test3 import Tests3
from Test.ObjectDetectionTest.test4 import Tests4
from Test.ObjectDetectionTest.test5 import Tests5
from Test.ObjectDetectionTest.test6 import Tests6
from Test.ObjectDetectionTest.test7 import Tests7
from Test.ObjectDetectionTest.test8 import Tests8
from Test.ObjectDetectionTest.test9 import Tests9
from Test.ObjectDetectionTest.test10 import Tests10
from Test.ObjectDetectionTest.test11 import Tests11
from Test.ObjectDetectionTest.test12 import Tests12

def run_all():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test_case in (InitialTests, Tests1, Tests2, Tests3, Tests4, Tests5, Tests6, Tests7, Tests8, Tests9, Tests10, Tests11, Tests12):
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Failures: {len(result.failures)}, Errors: {len(result.errors)}")

run_all()

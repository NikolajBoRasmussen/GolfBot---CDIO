import sys
import os
from ultralytics import YOLO
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ImageRecognitionModule.ObjectSetter import set_objects
from ImageRecognitionModule.ObjectGetter import get_objects, get_white_balls

#Test balls 
model = YOLO('Models/New Training 1/weights/best.onnx', task = "detect")

class SampleTests(unittest.TestCase):
    def setUp(self):
        self.predResult = model.predict("test.jpg") # Predict on a test image
        self.orange_ball, self.egg, self.white_balls, self.cross, self.robot = set_objects(self.predResult)

    def test_prediction(self):
        self.assertIsNotNone(self.predResult)
        self.assertGreater(len(self.predResult), 0)

    def test_can_find_objects(self):
        self.assertTrue(self.orange_ball is not None or self.egg is not None or self.white_balls is not None or self.cross is None or self.robot is None)

    def test_can_find_correct_amount(self):
        self.assertEqual(len(self.white_balls), 8)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed. Failures: {len(result.failures)}, Errors: {len(result.errors)}")

# Automatically run the tests if the module is imported or executed
run_tests()

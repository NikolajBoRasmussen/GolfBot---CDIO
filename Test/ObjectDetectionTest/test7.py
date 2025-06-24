import sys
import os
from ultralytics import YOLO
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ImageRecognitionModule.ObjectSetter import set_objects

#Test balls 
model = YOLO('Models/New Training 1/weights/best.onnx', task = "detect")

class Tests7(unittest.TestCase):
    def setUp(self):
        test_image_path = os.path.join(os.path.dirname(__file__), "test7.jpg")
        self.predResult = model.predict(test_image_path) # Predict on a test image
        self.cross, self.egg, self.robot, self.orange_ball, self.white_balls = set_objects(self.predResult)

    def test_prediction(self):
        self.assertIsNotNone(self.predResult)
        self.assertGreater(len(self.predResult), 0)

    def test_can_find_objects(self):
        self.assertTrue(self.orange_ball is None or self.egg is None or self.white_balls is None or self.cross is not None or self.robot is None)

    def test_can_find_correct_amount(self):
        amount_of_white_balls = 0
        for ball in self.white_balls:
            if ball is not None:
                amount_of_white_balls += 1

        self.assertEqual(amount_of_white_balls, 0)
        
    def test_can_find_correct_amount_of_egg(self):
        amount_of_egg = 0
        for box in self.predResult[0].boxes:
            if box.cls == 1:
                amount_of_egg += 1
        self.assertEqual(amount_of_egg, 0)
    
    def test_can_find_correct_amount_of_cross(self):
        amount_of_cross = 0
        for box in self.predResult[0].boxes:
            if box.cls == 0:
                amount_of_cross += 1
        self.assertEqual(amount_of_cross, 1)
    
    def test_can_find_correct_amount_of_robot(self):
        amount_of_robot = 0
        for box in self.predResult[0].boxes:
            if box.cls == 3:
                amount_of_robot += 1
        self.assertEqual(amount_of_robot, 0)

    def test_can_find_correct_amount_of_orange_ball(self):
        amount_of_orange_ball = 0
        for box in self.predResult[0].boxes:
            if box.cls == 2:
                amount_of_orange_ball += 1
        self.assertEqual(amount_of_orange_ball, 0)

    def tearDown(self):
        return super().tearDown()
import random
import unittest

from dui.types.emotion import Emotion


class Testintensity(unittest.TestCase):
    def setUp(self) -> None:
        self.emotion = Emotion()
        for i in range(1, 5 + 1):
            self.emotion[i] = random.randint(0, self.emotion._max_value)
        return super().setUp()

    def assertSignEqual(self, first, second, msg=None):
        self.assertEqual(first >= 0, second >= 0, msg)

    def test_magnitude_of_intensity(self):
        emotion1 = Emotion()
        emotion2 = Emotion()
        emotion1._value = [0, 300, 300, 300, 400, 400]
        emotion2._value = [0, 200, 300, 300, 400, 400]

        self.assertGreater(emotion1.intensity, emotion2.intensity)

        emotion1._value = [0, 100, 100, 200, 500, 200]
        emotion2._value = [0, 100, 100, 200, 500, 200]

        self.assertEqual(emotion2.intensity, emotion1.intensity)

        emotion1._value = [0, 0, 0, 100, 0, 0]
        emotion2._value = [0, 200, 300, 300, 400, 400]

        self.assertGreater(emotion2.intensity, emotion1.intensity)

        emotion1._value = [0, 100, 100, 100, 100, 100]
        emotion2._value = [0, 100, 300, 100, 100, 100]

        self.assertGreater(emotion2.intensity, emotion1.intensity)

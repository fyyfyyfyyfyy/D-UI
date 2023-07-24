import random
import unittest

from dui.types.person import Desire


class TestAbstractLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.desire = Desire()
        for i in range(1, 29 + 1):
            self.desire[i] = random.randint(0, 100)
        return super().setUp()

    def test_second_layer(self):
        ref = self.desire.second_layer
        val = self.desire._value

        self.assertEqual(ref[1], max(val[1], val[2]))
        self.assertEqual(ref[2], max(val[3], val[4]))
        self.assertEqual(ref[3], max(val[5], val[6]))
        self.assertEqual(ref[4], max(val[7], val[8]))
        self.assertEqual(ref[5], max(val[9], val[10], val[11]))
        self.assertEqual(ref[6], max(val[12], val[13], val[14]))
        self.assertEqual(ref[7], max(val[15], val[16], val[17]))
        self.assertEqual(ref[8], max(val[18], val[19]))
        self.assertEqual(ref[9], max(val[20], val[21]))
        self.assertEqual(ref[10], max(val[22], val[23]))
        self.assertEqual(ref[11], max(val[24], val[25]))
        self.assertEqual(ref[12], max(val[26], val[27]))
        self.assertEqual(ref[13], max(val[28], val[29]))

    def test_first_layer(self):
        ref = self.desire.first_layer
        val = self.desire._value

        self.assertEqual(ref[1], max(val[1:9]))
        self.assertEqual(ref[2], max(val[9:22]))
        self.assertEqual(ref[3], max(val[22:]))

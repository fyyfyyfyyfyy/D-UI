import unittest
from decimal import Decimal

from dui.types import Desire, Emotion


@unittest.skip('TODO: rewrite')
class TestPerson(unittest.TestCase):
    def test_example(self):
        desire = Desire()
        desire[1] = 1
        desire[2] = 1.5
        desire[29] = 2
        self.assertEqual(desire.second_layer[1], 1.5)
        self.assertEqual(desire.first_layer[1], 1.5)
        self.assertEqual(desire.first_layer[3], 2)

        # 测试加减乘除
        emotion1 = Emotion()
        self.assertIsInstance(emotion1._value, list)
        for i in range(1, 6):
            emotion1[i] = i + 1

        emotion2 = Emotion()
        for i in range(1, 6):
            emotion2[i] = i + 2

        add_res = emotion1 + emotion2
        sub_res = emotion1 - emotion2
        mul_res = emotion1 * 2.2

        for i in range(emotion1._item_count + 1):
            self.assertEqual(add_res[i], emotion1[i] + emotion2[i])
            self.assertEqual(sub_res[i], emotion1[i] - emotion2[i])
            self.assertEqual(mul_res[i], emotion1[i] * Decimal(2.2))

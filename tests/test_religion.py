import unittest

from dui.types.person import Desire, Feeling
from dui.types.religion import DesireWeight, Religion


class TestDesireWeight(unittest.TestCase):
    def test_init_desire_count(self):
        desire_weight = DesireWeight()
        self.assertEqual(desire_weight._item_count, Desire.DESIRE_COUNT)

    def test_get_item(self):
        desire_weight = DesireWeight()
        for i in range(1, Desire.DESIRE_COUNT + 1):
            self.assertEqual(desire_weight[i], 0)

    def test_set_item(self):
        desire_weight = DesireWeight()
        for i in range(1, Desire.DESIRE_COUNT + 1):
            desire_weight[i] = 10
            self.assertEqual(desire_weight[i], 10)


class TestReligion(unittest.TestCase):
    def test_init_default_values(self):
        religion = Religion(desc="吃咸舒适")
        self.assertEqual(religion._description, "吃咸舒适")
        self.assertIsInstance(religion._feeling, Feeling)
        self.assertIsInstance(religion._desire_weight, DesireWeight)

    def test_init_custom_values(self):
        feeling = Feeling()
        desire_weight = DesireWeight()
        religion = Religion(desc="吃酸舒适", feeling=feeling, desire_weight=desire_weight)
        self.assertEqual(religion._description, "吃酸舒适")

    def test_str_method(self):
        religion = Religion(desc="吃咸舒适")
        self.assertEqual(str(religion), "吃咸舒适")

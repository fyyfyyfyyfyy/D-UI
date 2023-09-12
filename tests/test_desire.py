import random
import unittest
from decimal import Decimal

from dui.types.desire import (Desire, DesireItem, _data_to_desire_tree,
                              _dict_to_desire_item)


class TestAbstractLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.desire = Desire()
        for i in range(1, 29 + 1):
            self.desire[i] = random.randint(0, 100)
        return super().setUp()

    def test_second_layer(self):
        ref = self.desire.second_layer
        val = self.desire.third_layer

        self.assertEqual(ref[1], max(val[1], val[2]))
        self.assertEqual(ref[2], max(val[3], val[4]))
        self.assertEqual(ref[3], max(val[5], val[6]))
        self.assertEqual(ref[4], max(val[7], val[8]))
        self.assertEqual(ref[5], max(val[9], val[10], val[11]))
        self.assertEqual(ref[6], max(val[12], val[13], val[14], val[15]))
        self.assertEqual(ref[7], max(val[16], val[17], val[18]))
        self.assertEqual(ref[8], max(val[19], val[20]))
        self.assertEqual(ref[9], max(val[21], val[22]))
        self.assertEqual(ref[10], max(val[23], val[24]))
        self.assertEqual(ref[11], max(val[25], val[26]))
        self.assertEqual(ref[12], max(val[27], val[28]))
        self.assertEqual(ref[13], val[29])


class TestDesireItem(unittest.TestCase):
    def test_value_with_child_items(self):
        subitem1 = DesireItem("2", "Subitem1", "Code2", 2, value=5)
        subitem2 = DesireItem("3", "Subitem2", "Code3", 2, value=8)
        item = DesireItem("1", "Item1", "Code1", 1, [subitem1, subitem2], value=10)
        self.assertEqual(item.value, Decimal(10))


class TestDesireFunctions(unittest.TestCase):

    def test_dict_to_desire_item(self):
        data = {
            "id": "D1",
            "name": "Desire1",
            "code": "D1",
            "items": [
                {
                    "id": "D1.1",
                    "name": "Sub-Desire1.1",
                    "code": "SD1.1",
                    "items": []
                }
            ]
        }

        desire_item = _dict_to_desire_item(data, 1)

        self.assertEqual(desire_item.id, "D1")
        self.assertEqual(desire_item.name, "Desire1")

    def test_data_to_desire_tree(self):
        data = [
            {
                "id": "D1",
                "name": "Desire1",
                "code": "D1",
                "items": []
            },
            {
                "id": "D2",
                "name": "Desire2",
                "code": "D2",
                "items": []
            }
        ]

        desire_tree = _data_to_desire_tree(data)

        self.assertEqual(desire_tree.id, "DROOT")
        self.assertEqual(desire_tree.name, "ROOT")


class TestDesire(unittest.TestCase):

    def setUp(self):
        self.desire = Desire()

    @unittest.skip('TODO: rewrite')
    def test_third_layer(self):
        expected_values = [
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
            200, 210, 220, 230, 240, 250, 260, 270, 280, 290
        ]
        self.desire.third_layer = [
            10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
            200, 210, 220, 230, 240, 250, 260, 270, 280, 290
        ]
        self.assertEqual(self.desire.third_layer, expected_values)

    def test_set_item(self):
        index = 1
        expected_value = Decimal(42)
        self.desire[index] = expected_value
        self.assertEqual(self.desire._id2nodes[f"D{index}"]._value, expected_value)

    @unittest.skip('bad test condition')
    def test_repr(self):
        self.desire[1] = 10
        self.desire[3] = 30
        expected_repr = "{'活着': 10, '吃': 30}"
        self.assertEqual(repr(self.desire), expected_repr)

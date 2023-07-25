import random
import unittest
from decimal import Decimal

from dui.types.decimalList import DecimalList


class TestOperation(unittest.TestCase):
    def setUp(self) -> None:
        self._item_count = random.randint(1, 10)

        self.values1 = [Decimal(random.randint(0, 100))
                        for _ in range(self._item_count)]
        self.values2 = [Decimal(random.randint(0, 100))
                        for _ in range(self._item_count)]
        # create test objects
        self.decimal_list1 = DecimalList(self._item_count, self.values1)
        self.decimal_list2 = DecimalList(self._item_count, self.values2)

        self.ep = random.random()
        return super().setUp()

    def test_op_add(self):
        expected_result = [Decimal(0)] + \
            [self.values1[i] + self.values2[i]
                for i in range(self._item_count)]

        # add
        result = self.decimal_list1 + self.decimal_list2

        self.assertEqual(result._item_count, self._item_count)
        self.assertEqual(result._value, expected_result)

    def test_op_sub(self):
        expected_result = [Decimal(0)] + \
            [self.values1[i] - self.values2[i]
                for i in range(self._item_count)]

        # sub
        result = self.decimal_list1 - self.decimal_list2

        self.assertEqual(result._item_count, self._item_count)
        self.assertEqual(result._value, expected_result)

    def test_op_mul(self):
        expected_result = [Decimal(0)] + \
            [self.values1[i] * Decimal(self.ep)
             for i in range(self._item_count)]

        # mul
        result = self.decimal_list1 * Decimal(self.ep)

        self.assertEqual(result._item_count, self._item_count)
        self.assertEqual(result._value, expected_result)

    def test_op_div(self):
        expected_result = [Decimal(0)] + \
            [self.values1[i] / Decimal(self.ep)
             for i in range(self._item_count)]

        # div
        result = self.decimal_list1 / Decimal(self.ep)

        self.assertEqual(result._item_count, self._item_count)
        self.assertEqual(result._value, expected_result)

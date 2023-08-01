import random
import unittest
from decimal import Decimal

from dui.types.decimalList import DecimalList


class TestInitDecimalList(unittest.TestCase):
    def test_get_item_value(self):
        decimallist = DecimalList(item_count=29)
        for i in range(1, decimallist._item_count + 1):
            self.assertEqual(decimallist[i], 0)

    def test_get_item_value2(self):
        values = []
        for i in range(1, 30):
            values.append(i)
        decimallist = DecimalList(item_count=29, item_values=values)
        for i in range(1, decimallist._item_count + 1):
            self.assertEqual(decimallist[i], values[i - 1])

    def test_get_item_value3(self):
        values = [0]
        for i in range(1, 30):
            values.append(i)
        decimallist = DecimalList(
            item_count=29, item_values=values, raw_data_flag=True)
        for i in range(1, decimallist._item_count + 1):
            self.assertEqual(decimallist[i], values[i])

    def test_set_item_value(self):
        decimallist = DecimalList(item_count=29)
        for i in range(1, decimallist._item_count + 1):
            decimallist[i] = 10
            self.assertEqual(decimallist[i], 10)

    def test_get_item_name(self):
        decimallist = DecimalList(item_count=29)
        self.assertEqual(decimallist._item_names, {})

    def test_get_item_name2(self):
        names = {}
        for i in range(0, 30):
            names[i] = str(i)
        decimallist = DecimalList(item_count=29, item_names=names)
        for i in range(1, decimallist._item_count + 1):
            self.assertEqual(decimallist._item_names[i], names[i - 1])

    def test_get_item_name3(self):
        names = {}
        for i in range(0, 30):
            names[i] = str(i)
        decimallist = DecimalList(
            item_count=29, item_names=names, raw_data_flag=True)
        for i in range(0, decimallist._item_count + 1):
            self.assertEqual(decimallist._item_names[i], names[i])


class TestPassingPara(unittest.TestCase):
    def setUp(self) -> None:
        self.decimal_list1 = DecimalList(item_count=29)
        self.decimal_list2 = DecimalList(item_count=29)
        self.decimal_list3 = DecimalList(item_count=29, raw_data_flag=True)
        self.decimal_list4 = DecimalList(item_count=29, raw_data_flag=True)

        return super().setUp()

    def test_allempty(self):
        decimallist3 = self.decimal_list1 + self.decimal_list2
        self.assertFalse(self.decimal_list1._raw_data_flag)
        self.assertFalse(self.decimal_list1._raw_disp_flag)

        self.assertFalse(self.decimal_list2._raw_data_flag)
        self.assertFalse(self.decimal_list2._raw_disp_flag)

        self.assertTrue(decimallist3._raw_data_flag)
        self.assertTrue(decimallist3._raw_disp_flag)

    def test_singleempty(self):
        decimallist3 = self.decimal_list1 + self.decimal_list3
        self.assertFalse(self.decimal_list1._raw_data_flag)
        self.assertFalse(self.decimal_list1._raw_disp_flag)

        self.assertTrue(self.decimal_list3._raw_data_flag)
        self.assertTrue(self.decimal_list3._raw_disp_flag)

        self.assertTrue(decimallist3._raw_data_flag)
        self.assertTrue(decimallist3._raw_disp_flag)

    def test_noneempty(self):
        decimallist3 = self.decimal_list3 + self.decimal_list4
        self.assertTrue(self.decimal_list3._raw_data_flag)
        self.assertTrue(self.decimal_list3._raw_disp_flag)

        self.assertTrue(self.decimal_list4._raw_data_flag)
        self.assertTrue(self.decimal_list4._raw_disp_flag)

        self.assertTrue(decimallist3._raw_data_flag)
        self.assertTrue(decimallist3._raw_disp_flag)

    def test_debug(self):
        decimallist0 = DecimalList(item_count=29, raw_disp_flag=True)
        decimallist3 = decimallist0 + self.decimal_list1
        self.assertFalse(decimallist0._raw_data_flag)
        self.assertTrue(decimallist0._raw_disp_flag)

        self.assertFalse(self.decimal_list1._raw_data_flag)
        self.assertFalse(self.decimal_list1._raw_disp_flag)

        self.assertTrue(decimallist3._raw_data_flag)
        self.assertTrue(decimallist3._raw_disp_flag)


class TestOperation(unittest.TestCase):
    def setUp(self) -> None:
        self._item_count = random.randint(1, 10)

        self.values1 = [Decimal(random.randint(0, 100))
                        for _ in range(self._item_count)]
        self.values2 = [Decimal(random.randint(0, 100))
                        for _ in range(self._item_count)]
        # create test objects
        self.decimal_list1 = DecimalList(
            self._item_count, item_values=self.values1)
        self.decimal_list2 = DecimalList(
            self._item_count, item_values=self.values2)

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

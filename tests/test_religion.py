import unittest

from dui.types.desire import DesireItem
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
    def test_create_successes(self):
        instance1 = Religion(desc="我相信/认为伴侣是舒服的", desire_name="伴侣")
        instance2 = Religion(desc="我相信/认为危险是不舒服的", desire_name="危险", valence=False)
        # 断言类实例是否创建成功
        self.assertIsInstance(instance1, Religion)
        self.assertIsInstance(instance2, Religion)

    def test_create_fails(self):
        # 测试直接创建失败
        with self.assertRaises(Exception):
            Religion(desc="吃咸舒适")
            Religion(desc="吃咸舒适", desire_name="aa")

    def test_init_default_values(self):
        religion = Religion(desc="我相信/认为吃咸是舒服的", desire_name="吃咸")
        self.assertEqual(religion._description, "我相信/认为吃咸是舒服的")
        self.assertIsInstance(religion._feeling, Feeling)
        self.assertIsInstance(religion._desire_weight, DesireWeight)

    def test_init_custom_values(self):
        feeling = Feeling()
        desire_weight = DesireWeight()
        religion = Religion(desc="吃酸舒适", desire_name="吃酸",
                            feeling=feeling, desire_weight=desire_weight)
        self.assertEqual(religion._description, "我相信/认为吃酸是舒服的")

    def test_str_method(self):
        religion = Religion(desc="吃咸舒适", desire_name="吃咸")
        self.assertEqual(str(religion), "我相信/认为吃咸是舒服的")

    def test_DesireItem_to_religion(self):
        subitem1 = DesireItem("DN", "本能", "NL1", 1)
        subitem2 = DesireItem("DS3", "物质", "SL2", 2)
        subitem3 = DesireItem("D23", "悦己", "DL3", 3)
        subitem4 = DesireItem("D2303", "呵护自己", "DL4", 4, parent=subitem3)
        subitem = [subitem1, subitem2, subitem3, subitem4]
        root = ["DN", "DS", "DD", "DD", "DS"]
        for i in range(4):
            religion = Religion(desire_item=subitem[i])
            self.assertEqual(religion._desire_name, subitem[i].name)
            self.assertEqual(religion._root_id, root[i])

    def test_Desire_to_religion(self):
        desire = Desire()
        desire[2] = 85
        desire[3] = 30
        # print(type(eval(desire.__repr__())))
        for des in eval(desire.__repr__()):
            religion = Religion(desire_name=des)
            self.assertEqual(religion._root_id, "DN")

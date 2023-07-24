import unittest
from datetime import datetime

from dui.types.event import Event
from dui.types.religion import Religion


class TestEvent(unittest.TestCase):

    def test_event_repr(self):
        location = "上海南路123号"
        environment = "海鲜餐厅"
        time = datetime(2023, 7, 22, 19, 30, 0)
        religion = Religion("吃辣舒适")

        event = Event(
            location=location,
            environment=environment,
            time=time,
            religion=religion
        )

        expected_repr = (
            f"  Location: {location}\n"
            f"  Environment: {environment}\n"
            f"  Time: {time}\n"
            f"  Religion: {religion}"
        )

        self.assertEqual(repr(event), expected_repr)

    def test_event_str(self):
        location = "上海南路123号"
        environment = "海鲜餐厅"
        time = datetime(2023, 7, 22, 19, 30, 0)
        religion = Religion("吃辣舒适")

        event = Event(
            location=location,
            environment=environment,
            time=time,
            religion=religion
        )

        expected_str = (
            "{\n"
            "  \"Event\": {\n"
            "    \"Location\": \"上海南路123号\",\n"
            "    \"Environment\": \"海鲜餐厅\",\n"
            "    \"Time\": \"2023-07-22 19:30:00\",\n"
            "    \"Religion\": {\n"
            "      \"desc\": \"吃辣舒适\"\n"
            "    }\n"
            "  }\n"
            "}"
        )

        self.assertEqual(str(event), expected_str)

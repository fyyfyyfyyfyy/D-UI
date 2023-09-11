import unittest

from dui.types import Desire, Emotion, Feeling
from dui.types.emotion import EMOTION_NAMES
from dui.types.person import Person
from dui.types.response_change import ResponseChange


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.desire = Desire
        self.emotion = Emotion()
        self.feeling = Feeling()
        self.person = Person(self.desire, self.emotion, self.feeling)

    def test_apply_response_change(self):
        answer = """
        这是一些文本。在这里包含一个 JSON 部分：

        ```json
        {
        "religion": "吃辣让人舒适",
        "emotion_delta": {
            "happy": 10,
            "sad": 3,
            "hate": 0,
            "amazed": 0,
            "angry": 0
        }
        }
        ```
        """
        response_change = ResponseChange(answer)

        self.person.emotion.set_emotion_value("happy", 5)
        self.person.emotion.set_emotion_value("sad", 3)

        self.person.apply_response_change(response_change)

        expected_results = [15, 6, 0, 0, 0]

        for en in EMOTION_NAMES:
            self.assertAlmostEqual(
                self.person.emotion.get_emotion_value(en),
                expected_results[EMOTION_NAMES.index(en)],
                places=2,
            )

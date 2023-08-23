import unittest

from dui.types.demand import Desire, Emotion, Feeling
from dui.types.person import Person
from dui.types.response_change import ResponseChange


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.desire = Desire
        self.emotion = Emotion()
        self.feeling = Feeling()
        self.person = Person(self.desire, self.emotion, self.feeling)

    def test_apply_response_change(self):
        answer = '''
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
        '''
        response_change = ResponseChange(answer)

        self.person.emotion.__setitem__(0, 5)
        self.person.emotion.__setitem__(1, 3)

        self.person.apply_response_change(response_change)

        self.assertAlmostEqual(self.person.emotion.__getitem__(0), 15, places=2)
        self.assertAlmostEqual(self.person.emotion.__getitem__(1), 6, places=2)

        self.assertAlmostEqual(self.person.emotion.__getitem__(2), 0, places=2)
        self.assertAlmostEqual(self.person.emotion.__getitem__(3), 0, places=2)
        self.assertAlmostEqual(self.person.emotion.__getitem__(4), 0, places=2)

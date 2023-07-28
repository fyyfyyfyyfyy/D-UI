import unittest
from datetime import datetime

from dui.llm import LLM_inference, event_to_prompt
from dui.types import Desire, Emotion, Event, Person, Religion
from dui.types.demand import EMOTION_NAMES


class TestLLMInference(unittest.TestCase):
    def setUp(self) -> None:
        desire = Desire(item_values=[0, 85])
        emotion = Emotion(item_values=[30])
        person = Person(desire, emotion)

        event = Event(location="四川北路666号", environment="和好朋友去了川菜馆", time=datetime.now())

        religion_str = ['吃辣让人舒适', '吃辣让人难受', '学习让人快乐', '学习让人难受']
        religions = [Religion(rs) for rs in religion_str]

        prompt = event_to_prompt(event, person=person, religions=religions)
        self.prompt = prompt
        return super().setUp()

    def test_religion_exist(self):
        response = LLM_inference(question=self.prompt)
        self.assertIn('religion', response)

    def test_emotion_delta_exist(self):
        response = LLM_inference(question=self.prompt)
        self.assertIn('emotion_delta', response)

    def test_emotion_names_exist(self):
        response = LLM_inference(question=self.prompt)
        for en in EMOTION_NAMES:
            self.assertIn(en, response)

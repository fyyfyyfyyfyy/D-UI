import unittest
from datetime import datetime

from dui.llm import LLM_inference, event_to_prompt
from dui.llm.native import PROMPT_EVENT2RELIGION_AND_FEELING as SYSTEM_PROMPT
from dui.llm.native import \
    fake_LLM_completion_Event2Religion_feeling as fake_LLM_func
from dui.types import Desire, Emotion, Event, Person, Religion
from dui.types.emotion import EMOTION_NAMES


class TestLLMInference(unittest.TestCase):
    def setUp(self) -> None:
        desire = Desire()
        desire[2] = 85
        emotion = Emotion(item_values=[30])
        person = Person(desire, emotion)

        event = Event(location="四川北路666号", environment="和好朋友去了川菜馆", time=datetime.now())

        religions = [
            Religion(desire_name="食物", valence=True),
            Religion(desire_name="食物", valence=False),
            Religion(desire_name="学习", valence=True),
            Religion(desire_name="学习", valence=False),
        ]
        prompt = event_to_prompt(event, person=person, religions=religions)
        self.prompt = prompt
        return super().setUp()

    def test_religion_exist(self):
        response = LLM_inference(
            question=self.prompt,
            system_prompt=SYSTEM_PROMPT,
            fake_LLM_func=fake_LLM_func,
        )
        self.assertIn("religion", response)

    def test_emotion_delta_exist(self):
        response = LLM_inference(
            question=self.prompt,
            system_prompt=SYSTEM_PROMPT,
            fake_LLM_func=fake_LLM_func,
        )
        self.assertIn("emotion_delta", response)

    def test_emotion_names_exist(self):
        response = LLM_inference(
            question=self.prompt,
            system_prompt=SYSTEM_PROMPT,
            fake_LLM_func=fake_LLM_func,
        )
        for en in EMOTION_NAMES:
            self.assertIn(en, response)

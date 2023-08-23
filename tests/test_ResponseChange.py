import re
import unittest

from dui.types.response_change import ResponseChange


def is_number(s):
    pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
    return bool(re.match(pattern, str(s)))


class TestResponseChange(unittest.TestCase):

    def test_valid_json(self):
        answer = '''
        这是一些文本。在这里包含一个 JSON 部分：

        ```json
        {
        "religion": "吃辣让人舒适",
        "emotion_delta": {
            "happy": 7,
            "sad": 8,
            "hate": 0,
            "amazed": 0,
            "angry": 0
        }
        }
        ```
        '''
        response = ResponseChange(answer)
        result = response.get_parsed_json()
        expected_keys = ['happy', 'sad', 'hate', 'amazed', 'angry']
        self.assertCountEqual(expected_keys, result.keys())
        for key in expected_keys:
            self.assertIsNotNone(result[key])
            self.assertTrue(is_number(result[key]), f"'{key}' is disabled")

    def test_initialization(self):
        answer = '''
        这是一些文本。在这里包含一个无效的 JSON 部分：
        ```json
        {
        "religion": "吃辣让人舒适",
        "emotion_delta": {
            "happy": "7",
            "sad": "8",
            "hate": "0",
            "amazed": "0",
            "angry": "0"
        }
        ```
        '''
        response = ResponseChange(answer)
        self.assertIsInstance(response.json_content, str)
        self.assertIsInstance(response.answer, str)

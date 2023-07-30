import json
import unittest

from dui.llm import ResponseChange


class TestResponseChange(unittest.TestCase):

    def test_valid_json(self):
        answer = '''
        这是一些文本。在这里包含两个 JSON 部分：
        {"happy": 5, "sad": 0, "hate": 0, "amazed": 0, "angry": 0}
        这是另一个 JSON 部分：
        {"happy": 10, "sad": -2, "hate": 0, "amazed": 3, "angry": 1}
        '''
        expected_result = {"happy": 10, "sad": -2, "hate": 0, "amazed": 3, "angry": 1}
        response = ResponseChange(answer)
        result = response.get_parsed_json()
        self.assertEqual(result, expected_result)

    def test_invalid_json(self):
        answer_invalid = '''
        这是一些文本。在这里包含一个无效的 JSON 部分：
        {"happy": +5, "sad": 0, "hate": 0, "amazed": 0, "angry": 0}
        '''
        response = ResponseChange(answer_invalid)
        self.assertRaises(json.JSONDecodeError, response.get_parsed_json)

    def test_initialization(self):
        response = ResponseChange('这里有一个 { "key": "value" }')
        self.assertIsInstance(response.match, list)
        self.assertIsInstance(response.pattern, str)
        self.assertIsInstance(response.answer, str)

import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from dui.types.emotion import EMOTION_NAMES_CN, Emotion
from dui.types.event import Event
from dui.types.history import HistoryItem
from dui.types.religion import Religion


@unittest.skip('需要修改')
class HistoryItemTestCase(unittest.TestCase):
    def test_from_dict(self):
        data = {
            'bg_event': '背景事件',
            'action': '动作',
            'event': {
                'location': '地点',
                'environment': '环境',
                'time': '2023-09-07T10:00:00'
            },
            'religion': {
                'desc': '信念描述',
                'desire_name': '欲望名称',
                'valence': True
            },
            'impact_emotion': {
                'emotion1': 0.5,
                'emotion2': 0.3
            },
            'impact_desire': {
                'desire1': 10,
                'desire2': 20
            },
            'num_desire': 5
        }

        # 预期对象
        expected_event = Event(
            location='地点',
            environment='环境',
            time=datetime(2023, 9, 7, 10, 0, 0)
        )
        expected_religion = Religion(
            desc='信念描述',
            desire_name='欲望名称',
            valence=True
        )
        expected_emotion = Emotion(EMOTION_NAMES_CN)
        expected_emotion.set_emotion_value('emotion1', Decimal('0.5'))
        expected_emotion.set_emotion_value('emotion2', Decimal('0.3'))

        with patch.object(
            Event, 'from_dict', return_value=expected_event
        ) as mock_event_from_dict, \
            patch.object(
                Religion, 'from_dict', return_value=expected_religion
        ) as mock_religion_from_dict:
            history_item = HistoryItem.from_dict(data)

        self.assertEqual(history_item.bg_event, '背景事件')
        self.assertEqual(history_item.action, '动作')
        self.assertEqual(history_item.event, expected_event)
        self.assertEqual(history_item.religion, expected_religion)
        self.assertEqual(history_item.impact_emotion, expected_emotion)
        self.assertEqual(history_item.impact_desire, {'desire1': 10, 'desire2': 20})
        self.assertEqual(history_item.num_desire, 5)

        # 验证 Event.from_dict 和 Religion.from_dict 是否以正确的参数被调用
        mock_event_from_dict.assert_called_once_with({
            'location': '地点',
            'environment': '环境',
            'time': '2023-09-07T10:00:00'
        })
        mock_religion_from_dict.assert_called_once_with({
            'desc': '信念描述',
            'desire_name': '欲望名称',
            'valence': True
        })


if __name__ == '__main__':
    unittest.main()

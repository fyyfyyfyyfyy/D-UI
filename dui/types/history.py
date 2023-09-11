import json
from datetime import datetime
from decimal import Decimal

from dui.types.emotion import EMOTION_NAMES_CN, Emotion
from dui.types.event import Event
from dui.types.religion import Religion


class History:
    @classmethod
    def from_data(cls, data: list) -> list["HistoryItem"]:
        return [HistoryItem.from_dict(item) for item in data]

    @classmethod
    def open(
        cls, file_path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> list["HistoryItem"]:
        with open(file_path, mode=mode, encoding=encoding) as f:
            raw_dict = json.load(f)

            return History.from_data(raw_dict)


class HistoryItem:
    def __init__(
        self,
        bg_event: str = None,
        action: str = "人工标记",
        event: Event = None,
        religion: Religion = None,
        impact_emotion: Emotion = None,
        impact_desire: dict = {},
        num_desire: int = 0,
    ):
        self.bg_event = bg_event
        self.action = action
        self.event = event
        self.religion = religion
        self.impact_emotion = impact_emotion
        self.impact_desire = impact_desire
        self.num_desire = num_desire

        self.record = {
            "bg_event": bg_event,
            "action": action,
            "event": event,
            "religion": religion,
            "impact_emotion": impact_emotion,
            "impact_desire": impact_desire,
            "num_desire": num_desire,
        }

    def __repr__(self) -> str:
        return repr(self.__dict__)

    def __str__(self) -> str:
        output_dict = {}
        output_dict["bg_event"] = self.bg_event
        output_dict["action"] = self.action
        output_dict["event"] = str(self.event)
        output_dict["religion"] = str(self.religion)
        output_dict["impact_emotion"] = str(self.impact_emotion)
        output_dict["impact_desire"] = str(self.impact_desire)
        output_dict["num_desire"] = str(self.num_desire)
        return str(output_dict)

    @classmethod
    def from_dict(cls, data) -> "HistoryItem":
        bg_event = data.get("bg_event")
        action = data.get("action")
        event_data = data.get("event")
        religion_data = data.get("religion")
        impact_emotion_data = data.get("impact_emotion")
        impact_desire = data.get("impact_desire", {})
        num_desire = data.get("num_desire", 0)

        event = Event.from_dict(event_data) if event_data else None
        religion = Religion.from_dict(religion_data) if religion_data else None
        impact_emotion = (
            Emotion.from_dict(impact_emotion_data) if impact_emotion_data else None
        )

        return cls(
            bg_event, action, event, religion, impact_emotion, impact_desire, num_desire
        )


def process_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    events = []  # 存储处理后的事件数据

    for item in json_data:
        json_content = item["背景事件内容"]["输入背景内容"]
        json_record = item["背景事件内容"]["记录事件"]

        # bg_event
        bg_event = json_content["事件内容分解"]["内容"]

        # action
        action = json_record["执行动作"]["人工/GPT推理"]

        # event
        event_location = ""
        event_time = datetime.now()
        # 将时间字典转化为datetime格式
        if "事件时间" in json_record:
            time_dict = json_record["事件时间"]
            # 此处时间默认值可能需要修改，应该不重要
            event_time = datetime(
                time_dict.get("年", 2023),
                time_dict.get("月", 8),
                time_dict.get("日", 20),
                time_dict.get("时", 0),
                time_dict.get("分", 0),
                time_dict.get("秒", 0),
            )
        # 将事件地点字典转化为字符串格式
        if "事件地点" in json_record:
            location_dict = json_record["事件地点"]
            event_location = "{}{}{}{}{}{}{}".format(
                location_dict.get("国家", ""),
                location_dict.get("省", ""),
                location_dict.get("市", ""),
                location_dict.get("县", ""),
                location_dict.get("街道", ""),
                location_dict.get("门牌号", ""),
                location_dict.get("地点文本", ""),
            )
        # 根据地点、背景、时间实例化 Event 类
        event_data = {
            "location": event_location,
            "environment": bg_event,
            "time": event_time,
        }
        event = Event.from_dict(event_data)

        # impact_desire
        desire_dict = json_record["欲望数据"]
        impact_desire = dict(list(desire_dict.items())[:5])

        # religion
        religion_dict = json_record["事件信念"]
        religion_desc = religion_dict["信念描述（标准语句）"]
        religion_desire_name = religion_dict["欲望"]
        religion_valence = True if religion_dict["信念核心"] == "有我" else False
        religion_data = {
            "desc": religion_desc,
            "desire_name": religion_desire_name,
            "valence": religion_valence,
        }
        Religion.from_dict(religion_data)

        # 该部分实现情绪变化量的累加
        impact_emotion = None
        if "事件关联感受数值" in json_record:
            impact_emotion_dict = json_record["事件关联感受数值"]
            impact_emotion = Emotion(EMOTION_NAMES_CN)
            for emotion, value in impact_emotion_dict.items():
                impact_emotion.set_emotion_value(emotion, Decimal(value * 0.01))

        # num_desire
        num_desire = int(desire_dict["欲望值"])

        # 统一进行赋值
        history_item_data = {
            "bg_event": bg_event,
            "action": action,
            "event": event,
            "religion": religion_data,
            "impact_emotion": impact_emotion,
            "impact_desire": impact_desire,
            "num_desire": num_desire,
        }
        history_item = HistoryItem.from_dict(history_item_data)

        events.append(history_item)

    return events

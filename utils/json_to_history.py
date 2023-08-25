import json
from datetime import datetime

from dui.types.emotion import Emotion
from dui.types.event import Event
from dui.types.history import History
from dui.types.religion import Religion


def json_to_history_list(json_file) -> list:
    with open(json_file, encoding="utf-8") as f:
        raw_dict = json.load(f)
    history_list = []
    for item in raw_dict:
        json_content = item['背景事件内容']['输入背景内容']
        json_record = item['背景事件内容']['记录事件']

        # 背景内容, Event类中的environment值
        bg_event = json_content['事件内容分解']['内容']

        # 执行动作
        action = json_record['执行动作']['人工/GPT推理']

        # Event类中的location值
        event_location = ""

        # Event类中的time值
        event_time = datetime.now()

        # 将时间字典转化为datetime格式
        if ('事件时间' in json_record):
            time_dict = json_record['事件时间']
            event_time = datetime(time_dict.get('年', 2023),
                                  time_dict.get('月', 8),
                                  time_dict.get('日', 20),
                                  time_dict.get('时', 0),
                                  time_dict.get('分', 0),
                                  time_dict.get('秒', 0)
                                  )

        # 将事件地点字典转化为字符串格式
        if ('事件地点' in json_record):
            location_dict = json_record['事件地点']
            event_location = '{}{}{}{}{}{}{}'.format(location_dict.get('国家', ""),
                                                     location_dict.get('省', ""),
                                                     location_dict.get('市', ""),
                                                     location_dict.get('县', ""),
                                                     location_dict.get('街道', ""),
                                                     location_dict.get('门牌号', ""),
                                                     location_dict.get('地点文本', "")
                                                     )

        # 根据地点、背景、时间实例化Event类
        event = Event(location=event_location, environment=bg_event, time=event_time)

        # 实例化Religion类
        religion_dict = json_record['事件信念']
        religion_desc = religion_dict['信念描述（标准语句）']
        religion_primer = religion_dict['引导语']
        religion_desire_name = religion_dict['欲望']
        religion_middle_word = religion_dict['中间词']
        religion_valence = True if religion_dict['信念核心'] == '有我' else False
        religion = Religion(desc=religion_desc,
                            primer=religion_primer,
                            desire_name=religion_desire_name,
                            middle_word=religion_middle_word,
                            valence=religion_valence
                            )
        impact_emotion_dict = json_record['事件关联感受数值']
        impact_emotion = Emotion(item_values=list(impact_emotion_dict.values()))

        # 记录欲望数据字典与欲望值
        desire_dict = json_record['欲望数据']
        impact_desire = dict(list(desire_dict.items())[:5])
        num_desire = int(desire_dict['欲望值'])
        history_event = History(bg_event=bg_event,
                                action=action,
                                event=event,
                                religion=religion,
                                impact_emotion=impact_emotion,
                                impact_desire=impact_desire,
                                num_desire=num_desire
                                )
        history_list.append(history_event)
    return history_list

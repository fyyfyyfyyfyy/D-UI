from dui.types.emotion import Emotion
from dui.types.event import Event
from dui.types.religion import Religion


class History():
    def __init__(self,
                 bg_event: str = None,
                 action: str = "人工标记",
                 event: Event = None,
                 religion: Religion = None,
                 impact_emotion: Emotion = None,
                 impact_desire: dict = {},
                 num_desire: int = 0
                 ):
        self.bg_event = bg_event
        self.action = action
        self.event = event
        self.religion = religion
        self.impact_emotion = impact_emotion
        self.impact_desire = impact_desire
        self.num_desire = num_desire

        self.record = {
            'bg_event': bg_event,
            'action': action,
            'event': event,
            'religion': religion,
            'impact_emotion': impact_emotion,
            'impact_desire': impact_desire,
            'num_desire': num_desire
        }

    def __repr__(self) -> str:
        return repr(self.__dict__)

    def __str__(self) -> str:
        output_dict = {}
        output_dict['bg_event'] = self.bg_event
        output_dict['action'] = self.action
        output_dict['event'] = str(self.event)
        output_dict['religion'] = str(self.religion)
        output_dict['impact_emotion'] = str(self.impact_emotion)
        output_dict['impact_desire'] = str(self.impact_desire)
        output_dict['num_desire'] = str(self.num_desire)
        return str(output_dict)

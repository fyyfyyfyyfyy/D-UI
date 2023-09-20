from __future__ import annotations

import json

from dui.types import Event, Person, Religion
from dui.utils.log import get_logger

logger = get_logger(__name__)


PROMPT_EVENT2RELIGION_AND_FEELING = """You play the role of a psychologist,\
and I will input a number of events, scenarios and my states (desires, emotions),\
as well as a list of beliefs from which\
you will need to select the one I am most likely to have given that event.\
Desires will be entered as key-value pairs with values [0,100],\
and emotions will be five dimensional vectors\
with values from 0 to 100 for each dimension,\
the five dimensions being "happy", "sad", "hate", "amazed", and "angry".\
Please reason about my mood changes based on them\
and consider only the effect of the belief on mood,\
ignoring other factors.\
Only the effect of this belief on mood should be considered,\
other factors have not been taken into account.\
Next is a case where I enter a list of beliefs as\
['Eating spicy food makes me happy', 'Eating spicy food makes me sad', \
'Studying makes me happy', 'Studying makes me sad'],\
for example, you need to output the following:
``` \
{"religion": "学习让人快乐", "emotion_delta": {\
"happy": 5, "sad": 0, "hate": 0, "amazed": 0, "angry": 0}} \
```\
Before each output you need to analyze the reasons for choosing beliefs \
and mood changes in 100 words.\
Next I start the first input.\
You must output the JSON format data of the example above.\
The output in JSON format is preceded and followed by the symbol '''
"""


def fake_LLM_completion_Event2Religion_feeling() -> str:
    logger.warning("fake_LLM_completion_Event2Religion_feeling is called.")
    return """在这个事件场景中，选择信念"吃辣让人舒适"。因为我们在川菜馆，\
川菜以辣味著称，对于喜欢辣的人来说，吃辣可以带来舒适的感觉。\
这个信念会对情绪产生影响，具体的情绪变化如下：

- 开心程度：增加5点，从30增加到35；
- 生气程度：不变，仍为0；
- 惊讶程度：不变，仍为0；
- 讨厌程度：不变，仍为0；
- 难过程度：不变，仍为0。

最终的情绪为{happy: 35, sad: 0, hate: 0, amazed: 0, angry: 0}，\
情绪的变化量为{happy: 5, sad: 0, hate: 0, amazed: 0, angry: 0}。\
输出的完整json如下：

```json
{
  "religion": "吃辣让人舒适",
  "emotion_delta": {
    "happy": 5,
    "sad": 0,
    "hate": 0,
    "amazed": 0,
    "angry": 0
  }
}
```"""


def event_to_prompt(
    event: Event, person: Person, religions: list[Religion] | None = None
) -> str:
    prompt_dict = {
        "要推理的事件场景": event,
        "初始情绪": person._emotion,
        "初始欲望": person._desire,
    }
    if religions is not None:
        religions_str = json.dumps([str(r) for r in religions], ensure_ascii=False)
        prompt_dict["信念列表"] = religions_str
    prompt = ",".join([f"{k}为{v}" for k, v in prompt_dict.items()])
    return prompt


def raw_event_to_str(background: str, emotions: str, desire: str, belief_list: str):
    event = "事件和场景为%s,初始情绪为%s,初始欲望为%s,信念列表为%s." % (
        background,
        emotions,
        desire,
        belief_list,
    )
    json_limit = (
        "请推理信念以及情绪变化,输出仅给出JSON, JSON格式示例:"
        '{"belief": "学习", "emotion_change": {"happiness": +5, "anger": 0,'
        'surprise": 0, "disgust": 0, "sadness": 0}}'
    )
    return event + json_limit

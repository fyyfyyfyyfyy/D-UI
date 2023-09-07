from __future__ import annotations

import json
import os
import re

import openai  # type: ignore

from dui.types import Event, Person, Religion
from dui.utils.log import get_logger

logger = get_logger(__name__)


class ResponseChange:
    def __init__(self, answer: str):
        self.answer = answer
        self.pattern = r'{[^{}]*}'
        self.match = re.findall(self.pattern, self.answer)

    def get_parsed_json(self):
        if self.match:
            last_match = self.match[-1]
            try:
                json_data = json.loads(last_match)
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
                return json_data
            except json.JSONDecodeError as e:
                raise e


def has_envvar(name: str):
    env_var = os.getenv(name)
    if env_var is None or len(env_var) <= 0:
        return False
    return True


openai.api_key = os.getenv('OPENAI_API_KEY')

if not has_envvar('https_proxy'):
    openai.api_base = "https://openkey.cloud/v1"  # 换成代理，一定要加v1

SYSTEM_PROMPT = '''You play the role of a psychologist,\
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
The output in JSON format is preceded and followed by the symbol \'''
'''


# def build_system_prompt():
#     json_output = {
#         'religion': '学习让人快乐',
#         'emotion_delta': dict([(name, 5 if i == 0 else 0)
# for (i, name) in enumerate(EMOTION_NAMES)])
#     }
#     json_limit = f"""请推理信念以及情绪变化,输出仅给出JSON, JSON格式示例:
# ```
# {json.dumps(json_output, ensure_ascii=False)}
# ```"""
#     return json_limit

def fake_LLM_completion() -> str:
    logger.warning('WARNING: fake LLM completion is called.')
    return '''在这个事件场景中，选择信念"吃辣让人舒适"。因为我们在川菜馆，\
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
```'''


def GPT_completion(question, history, user='user',
                   model='gpt-3.5-turbo', system_prompt=SYSTEM_PROMPT) -> str:
    question = "事件场景历史为:" + ','.join(str(history[-3:])) + "。" + question

    completion = openai.ChatCompletion.create(
        model=model,  # gpt-3.5-turbo, gpt-4 ...
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": user, "content": question}]
    )
    return completion.choices[0].message.content


def LLM_inference(question, history, user='user',
                  model='gpt-3.5-turbo', system_prompt=SYSTEM_PROMPT):
    if has_envvar('OPENAI_API_KEY'):
        return GPT_completion(question=question, history=history, user=user,
                              model=model, system_prompt=system_prompt)
    else:
        return fake_LLM_completion()


def event_to_prompt(event: Event, person: Person, religions: list[Religion]) -> str:
    religions_str = json.dumps([str(r) for r in religions], ensure_ascii=False)
    prompt_dict = {
        '要推理的事件场景': event,
        '初始情绪': person._emotion,
        '初始欲望': person._desire,
        '信念列表': religions_str
    }
    prompt = ','.join([f'{k}为{v}' for k, v in prompt_dict.items()])
    return prompt


def raw_event_to_str(background: str, emotions: str, desire: str, belief_list: str):
    event = '事件和场景为%s,初始情绪为%s,初始欲望为%s,信念列表为%s.' \
            % (background, emotions, desire, belief_list)
    json_limit = '请推理信念以及情绪变化,输出仅给出JSON, JSON格式示例:' \
        '{"belief": "学习", "emotion_change": {"happiness": +5, "anger": 0,' \
        'surprise": 0, "disgust": 0, "sadness": 0}}'
    return event + json_limit

from __future__ import annotations

import json
import os
import re

import openai  # type: ignore

from dui.types import Event, Person, Religion


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

SYSTEM_PROMPT = '''我会格式化输入一些事件、场景以及该事件、场景下我的欲望和情绪\
,我需要你在信念列表选择最符合的一个信念,注意,仅选择一个信念选项,\
并根据这个信念选项推理得出我的情绪的变化量.下面我对格式进行说明.\
下面定义欲望以及其量值：共有29个欲望,每个欲望为整数,范围0-100,\
数字越大欲望越大,0表示没有这个欲望.输入时我会以列表形式继进行输入,\
格式如下[0,0,0,0,...].29个欲望均并列,没有优先级,按顺序依次为：\
休息欲望、睡眠欲望、吃东西的欲望、喝东西的欲望、生存的欲望、\
死亡的欲望、实现自我圆满的欲望、实现自我意义的欲望、觉醒的欲望、\
好奇的欲望、思考的欲望、学习的欲望、付出的欲望、悦己的欲望、\
获得荣誉的欲望、获得成功的欲望、占有的欲望、获得权力的欲望、\
购买的欲望、收藏的欲望、获得金钱的欲望、感觉审美欲望、听觉审美欲望、\
视觉审美欲望、爱情欲望、亲情欲望、友情欲望、心理性欲、生理性欲.\
下面定义本次推理的信念列表：[吃辣让人舒适、吃辣让人难受、\
学习让人快乐、学习让人难受].下面定义事件和场景：\
事件和场景的格式为四元组(人物,地点,环境,时间).下面定义情绪,\
使用了一个五元组来描述,其中每个维度表示情绪的不同方面.\
数值范围是0-100的浮点数,变化时若超过100,则重置为0,\
所有维度都是0时表示情绪“平静”,以下是这个五元组的含义：维度1：\
开心程度,0-20时为'开心',20-40时为'快乐',40-60时为'幸福',\
60-80时为'狂喜',80-100时为'孤独'；维度2：生气程度,0-20时'生气',\
20-40时'愤怒',40-60时'仇恨',60-80时'疯癫',80-100时'茫然'；\
维度3：惊讶程度,0-20时'惊讶',20-40时'害怕',40-60时'恐惧',\
60-80时'惊恐',80-100时'麻木';维度4：讨厌程度,0-20时'讨厌',\
20-40时'厌恶',40-60时'烦躁',60-80时'焦虑',80-100时'空虚';\
维度5：难过程度,0-20时'难过',20-40时'悲伤',40-60时'沮丧',\
60-80时'绝望',80-100时'无助'.因此,举例来说,情绪[40,10,10,10,10]\
表示快乐、并有轻微的生气、惊讶、讨厌和难过情绪.最终的推理结果请以\
json格式返回,内容包括在信念列表中选择的信念、事件发生后,\
与输入的初始值相比,每个情绪的维度的最终值与变化量(如,增加10点记为10\
,减少10点记为-10).输出json格式为：\
``` \
{"religion": "学习让人快乐", "emotion_delta": {\
"happy": 5, "sad": 0, "hate": 0, "amazed": 0, "angry": 0}} \
```\
注意,给出的情绪、信念都是我的情绪和信念,\
请根据它们对我的情绪变化进行推理并只考虑信念对情绪的影响,忽略其它因素.\
只需考虑这个信念对情绪的影响,其他因素并未考虑在内.下面开始推理,\
用100字分析选择信念的原因与情绪的变化,并输出完整json。'''


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
    import sys
    print('WARNING: fake LLM completion is called.', file=sys.stderr)
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
    "happy": "5",
    "sad": "0",
    "hate": "0",
    "amazed": "0",
    "angry": "0"
  }
}
```'''


def GPT_completion(question, user='user',
                   model='gpt-3.5-turbo', system_prompt=SYSTEM_PROMPT) -> str:
    completion = openai.ChatCompletion.create(
        model=model,  # gpt-3.5-turbo, gpt-4 ...
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": user, "content": question}
        ]
    )
    return completion.choices[0].message.content


def LLM_inference(question, user='user',
                  model='gpt-3.5-turbo', system_prompt=SYSTEM_PROMPT):
    if has_envvar('OPENAI_API_KEY'):
        return GPT_completion(question=question, user=user,
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


if __name__ == "__main__":
    back = '(我和好朋友,四川北路666号,川菜馆,8:00pm)'
    emo = '[30,0,0,0,0]'
    des = '[0,0,85,75,60,0,40,40,0,30,0,0,0,0,0,0,0,0,70,0,0,60,60,60,0,0,80,0,0]'
    belief = '[吃辣让人舒适、吃辣让人难受、学习让人快乐、学习让人难受]'
    event = raw_event_to_str(background=back, emotions=emo,
                             desire=des, belief_list=belief)
    answer = GPT_completion(question=event)
    print(answer)

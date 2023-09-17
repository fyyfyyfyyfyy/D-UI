import json
import os
import time
from decimal import Decimal

import openai  # type: ignore
import yaml

from dui.types.desire import Desire
from dui.types.religion import Religion


def yaml2dict(path):
    with open(path, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data


DESIRE_DICT = yaml2dict('./data/desire.yml')


def has_proxy():
    proxy_addr = os.getenv('https_proxy')
    if proxy_addr is None or len(proxy_addr) <= 0:
        return False
    return True


openai.api_key = os.getenv('OPENAI_API_KEY')

if not has_proxy():
    openai.api_base = "https://openkey.cloud/v1"  # 换成代理，一定要加v1


def AskChatGPT(messages):
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
    )
    return response.choices[0].message.content


def ReligionPipeline(user, question, prompt):
    print("input:", question)
    with open(prompt, "r", encoding="utf-8") as f:
        condition = f.read()
    desire = Desire()
    desire._id2nodes['DN']._value = Decimal(300)
    desire_list = []
    for des in eval(desire.__repr__()):
        desire_list.append(des)
    condition = condition + str(desire_list)
    messages = [{"role": "system", "content": condition},
                {"role": user, "content": question}]
    ans1 = AskChatGPT(messages)
    # print(ans1)
    messages.append({"role": "system", "content": ans1})

    ans1 = json.loads(ans1)
    low_desire = ans1['desire']
    value = ans1['value']
    religion = Religion(desire_name=low_desire, valence=value)
    primer = religion._primer
    middle_word = religion._middle_word
    valence = religion._valence_str
    root = religion._root_id

    prompt2 = "确定了初级欲望后,现在有了一个更加细粒度的欲望列表,你需要再从中选一个最合适的,输出方式仅需输出你选择的欲望名称,现在的欲望列表如下:"

    high_desire = [low_desire]
    for l2 in DESIRE_DICT[{"DN": 0, "DS": 1, "DD": 2}.get(root, None)]['items']:
        for l3 in l2['items']:
            if l3['name'] == low_desire:
                for l4 in l3['items']:
                    high_desire.append(l4["name"])
                    for l5 in l4['items']:
                        high_desire.append(l5["name"])
    # print(high_desire)
    condition2 = prompt2 + str(high_desire)
    messages.append({"role": "user", "content": condition2})
    ans2 = AskChatGPT(messages)
    return primer + ans2 + middle_word + valence


if __name__ == "__main__":
    start = time.time()
    answer = ReligionPipeline(user='user', question='我好饿',
                              prompt='./utils/prompt_religion2.txt')
    end = time.time()
    print(answer)
    print("time", end - start)

import json
import time
from decimal import Decimal

import openai  # type: ignore

from dui.llm import LLM_inference
from dui.types import Desire, Religion
from dui.types.religion_feeling import map_religion_feeling
from dui.utils.data import load_data
from dui.utils.log import get_logger

logger = get_logger(__name__, console_level="DEBUG")

DESIRE_DICT = load_data("desire")


def AskChatGPT(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return response.choices[0].message.content


def ReligionPipeline(user, question, prompt) -> Religion:
    print("input:", question)

    desire = Desire()
    desire._id2nodes["DN"]._value = Decimal(300)
    desire_list = []
    for des in eval(desire.__repr__()):
        desire_list.append(des)
    condition1 = prompt + str(desire_list)

    ans1 = LLM_inference(question=question, system_prompt=condition1)
    chat_history = [
        {"role": "system", "content": condition1},
        {"role": user, "content": question},
    ]
    print("ans1\n", ans1)

    chat_history.append({"role": "system", "content": ans1})

    ans1 = json.loads(ans1)
    low_desire = ans1["desire"]
    valence = ans1["valence"]
    religion = Religion(desire_name=low_desire, valence=valence)
    root = religion._root_id

    prompt2 = """确定了初级欲望后,现在有了一个更加细粒度的欲望列表,你必须根据最近一次对话的事件从该列表中选一个最合适的,\
        输出格式必须为字典格式,key分别为"desire","id","valence"(desire表示欲望名,id取自desire对应的标识,valence表示正向或负向)，现在的欲望列表如下:"""

    high_desire_list = []
    for l2 in DESIRE_DICT[{"DN": 0, "DS": 1, "DD": 2}.get(root, None)]["items"]:
        for l3 in l2["items"]:
            if l3["name"] == low_desire:
                high_desire_list.append({l3["id"]: low_desire})
                for l4 in l3["items"]:
                    high_desire_list.append({l4["id"]: l4["name"]})
                    for l5 in l4["items"]:
                        high_desire_list.append({l5["id"]: l5["name"]})
    print(high_desire_list)
    condition2 = prompt2 + str(high_desire_list)
    ans2 = LLM_inference(question=condition2, chat_history=chat_history)
    # print("ans2:\n", ans2)
    ans2 = json.loads(ans2)
    high_desire = ans2["desire"]
    # ans2_id = ans2['id']
    ans2_valence = ans2["valence"]
    print(f"本次推理从{low_desire}中选取了{high_desire}作为欲望")
    res_religion = Religion(desire_name=high_desire, valence=ans2_valence)

    return res_religion


if __name__ == "__main__":
    while True:
        question = input("请输入事件：(输入quit结束运行~)\n")
        if question == "quit":
            break
        prompt = """你现在扮演一个资深的心理学家,你认为人的每一句话都能反应当时的欲望,\
因此你的任务是根据我给的一句话,必须从下面所给的29个初级欲望中选择最符合的一个,并输出\
该语句对应的欲望是正向还是负向(正向表示为true,负向表示为false,\
"我想吃"对于欲望"吃"就是正向的),你的输出形式为字典形式,key分别为\
"desire",""(desire表示欲望名,valence表示正向或负向)\
如{"desire": "吃", "valence": true},注意,\
你的输出仅包含最终的字典。29个初级欲望列表如下:"""

        start = time.time()
        answer: Religion = ReligionPipeline(
            user="user", question=question, prompt=prompt
        )
        end = time.time()
        print(answer)
        print(map_religion_feeling(answer))

        print("time", end - start)

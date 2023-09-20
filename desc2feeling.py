import json
import time
from decimal import Decimal

from dui.llm import ChatMessageItem, LLM_inference
from dui.types import Desire, Religion
from dui.types.religion_feeling import map_religion_feeling
from dui.utils.data import load_data
from dui.utils.log import get_logger

logger = get_logger("desc2feeling", console_level="DEBUG")

DESIRE_DICT = load_data("desire")

SYSTEM_PROMPT = """
你扮演一个担任自然语言表达动机提取工作AI程序。\
我将输入一句自然语言与欲望列表，你从我提供的欲望列表中，选择与该自然语言表达动机最匹配的一项欲望。\
你第一反应的欲望很可能不是最匹配的，因此你需要一步步思考。\
我希望您只在一个唯一的代码块内回复 json，而不是其他任何内容。\
不要写解释，除非我指示您这样做，否则不要自行追加新的输入。
输入格式分为两行，第一行是自然语言的句子，第二行是欲望列表。
输出格式为 json 格式的字典，含有的键为 `desire`（欲望名称，来自输入列表）和 `valence` （极性，true 积极 false 消极）
"""

QUESTION_TEMPLATE = """
自然语言：{}
欲望列表：{}
"""


def ReligionPipeline(user_input) -> Religion:
    logger.debug(f"用户输入问题 input: {user_input}")

    desire = Desire()
    desire._id2nodes["DN"]._value = Decimal(300)
    desire_list = []
    for des in eval(desire.__repr__()):
        desire_list.append(des)

    question = QUESTION_TEMPLATE.format(user_input, desire_list)

    chat_history: list[ChatMessageItem] = []
    ans1 = LLM_inference(
        question=question, system_prompt=SYSTEM_PROMPT, chat_history=chat_history
    )
    logger.debug(f"GPT推理 answer [1st]: {ans1}")

    ans1 = json.loads(ans1)
    low_desire = ans1["desire"]
    valence = ans1["valence"]
    religion = Religion(desire_name=low_desire, valence=valence)
    root = religion._root_id

    high_desire_list = []
    for l2 in DESIRE_DICT[{"DN": 0, "DS": 1, "DD": 2}.get(root, None)]["items"]:
        for l3 in l2["items"]:
            if l3["name"] == low_desire:
                high_desire_list.append(l3["name"])
                for l4 in l3["items"]:
                    high_desire_list.append(l4["name"])
                    for l5 in l4["items"]:
                        high_desire_list.append(l5["name"])

    logger.debug(f"备选欲望列表: {high_desire_list}")
    question_2 = QUESTION_TEMPLATE.format(user_input, str(high_desire_list))

    ans2 = LLM_inference(
        question=question_2, chat_history=chat_history, system_prompt=SYSTEM_PROMPT
    )
    logger.debug(f"GPT推理 answer [2nd]: {ans2}")

    ans2 = json.loads(ans2)
    high_desire = ans2["desire"]
    ans2_valence = ans2["valence"]

    logger.debug(f"信念选择 select: 本次推理从{low_desire}中选取了{high_desire}作为欲望")
    res_religion = Religion(desire_name=high_desire, valence=ans2_valence)

    return res_religion


if __name__ == "__main__":
    while True:
        question = input("请输入事件：(输入quit结束运行~)\n")
        if question == "quit":
            break

        start = time.time()
        answer: Religion = ReligionPipeline(user_input=question)
        end = time.time()
        logger.info(f"最终选择的信念 religion: {answer}")
        logger.debug(f"信念对应感受 feeling: {map_religion_feeling(answer)}")

        logger.debug(f"消耗的时间 cost_time: {end - start}")

        logger.info("本轮分析结束 [ROUND_END]")
        logger.info("-----------------------")

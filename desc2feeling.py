import json
import time

from dui.llm import ChatMessageItem, LLM_inference
from dui.types import Religion
from dui.types.desire import DESIRE_PROPERTY
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


def extract_religion(
    user_input: str, optional_desires: list[str], chat_history: list[ChatMessageItem]
) -> Religion:
    question = QUESTION_TEMPLATE.format(user_input, optional_desires)
    logger.debug(f"欲望备选：{optional_desires}")
    answer = LLM_inference(
        question=question, system_prompt=SYSTEM_PROMPT, chat_history=chat_history
    )
    try:
        religion_data = json.loads(answer)

        desire_name = religion_data["desire"]
        valence = religion_data["valence"]

        religion = Religion(desire_name=desire_name, valence=valence)
        logger.debug(f'信念选择：本次推理选择 "{ religion }" 作为信念')

    except json.decoder.JSONDecodeError as e:
        logger.warn("Failed to decode LLM inference answer")
        logger.warn(f"{e.msg}")
        religion = Religion(desire_name=answer)
    except Exception as e:
        logger.fatal("Unexpected Exception !!!")
        logger.fatal(f"{e}")
        religion = Religion(desire_name=answer)
    finally:
        return religion


if __name__ == "__main__":
    while True:
        user_input = input("请输入事件：(输入quit结束运行~)\n")
        if user_input == "quit":
            break

        start = time.time()

        chat_history: list[ChatMessageItem] = []

        logger.debug(f"用户输入问题 input: {user_input}")

        desire = DESIRE_PROPERTY
        desire_list = []
        for i in range(1, 30):
            item_name = desire._id2nodes[f"D{i}"].name
            desire_list.append(item_name)

        religion1 = extract_religion(user_input, desire_list, chat_history)

        high_desire_list = []

        high_desire_list.append(religion1._desire_item.name)
        for l4 in religion1._desire_item.items:
            high_desire_list.append(l4.name)
            for l5 in l4.items:
                high_desire_list.append(l5.name)

        religion2 = extract_religion(user_input, high_desire_list, chat_history)

        end = time.time()
        logger.info(f"最终选择的信念 religion: {religion2}")
        logger.debug(f"信念对应感受 feeling: {map_religion_feeling(religion2)}")

        logger.debug(f"消耗的时间 cost_time: {end - start}")

        logger.info("本轮分析结束 [ROUND_END]")
        logger.info("-----------------------")

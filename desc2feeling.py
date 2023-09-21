import json
import time
from typing import TypedDict

from device.asr import get_asr_response
from device.eilik import EilikCom
from dui.llm import ChatMessageItem, LLM_inference
from dui.types import Religion
from dui.types import emotion as name_lib
from dui.types.desire import DESIRE_PROPERTY, DesireItem
from dui.types.emotion import Feeling
from dui.types.religion_feeling import map_religion_feeling
from dui.utils.data import load_data
from dui.utils.log import get_logger

logger = get_logger("desc2feeling", console_level="DEBUG")

SYSTEM_PROMPT = """
你扮演一个担任自然语言表达动机提取工作AI程序。\
我将输入一句自然语言与欲望列表，你从我提供的欲望列表中，选择与该自然语言表达动机最匹配的一项欲望。\
同时，你需要判断表达者在说这句自然语言时的情绪状态是积极还是消极。\
你第一反应的欲望很可能不是最匹配的，因此你需要一步步思考。\
我希望你只在一个唯一的代码块内回复 json，而不是其他任何内容。\
不要写解释，除非我指示你这样做，否则不要自行追加新的输入。
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
        question=question,
        system_prompt=SYSTEM_PROMPT,
        chat_history=chat_history,
        model="gpt-4"
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


def console_input() -> str:
    user_input = input("请输入事件：(输入quit结束运行~)\n")
    if user_input == 'quit':
        exit(0)
    return user_input


class FEELING2ACTION_DATA_ITEM(TypedDict):
    feeling: str
    range_start: int
    range_end: int
    desc: str
    action_id: int


FEELING2ACTION_DATA: list[FEELING2ACTION_DATA_ITEM] = load_data("feeling2action")


ALL_EMOTION_NAMES = name_lib.EMOTION_NAMES + [name_lib.EMOTION_NAME_DEFAULT]
ALL_EMOTION_NAMES_CN = name_lib.EMOTION_NAMES_CN + [name_lib.EMOTION_NAME_DEFAULT_CN]

translate_emotion_name: dict[str, str] = dict(zip(ALL_EMOTION_NAMES_CN,
                                                  ALL_EMOTION_NAMES))

mapping_feeling_action: dict[str, list[FEELING2ACTION_DATA_ITEM]] = dict([
    (feeling_name,
     [item for item in FEELING2ACTION_DATA if
      translate_emotion_name[item['feeling']] == feeling_name]
     ) for feeling_name in ALL_EMOTION_NAMES
])


def feeling2eilik_action(feeling: Feeling) -> int:
    feeling_item = feeling.get_max_feeling_item(50)
    name, value = feeling_item

    optional_list = mapping_feeling_action[name]

    for i in optional_list:
        if i['range_start'] <= value < i['range_end']:
            return i['action_id']

    logger.warn('reach end of feeling2eilik_action')
    return mapping_feeling_action['calm'][0]["action_id"]


if __name__ == "__main__":
    desire = DESIRE_PROPERTY

    opened = EilikCom.open(port='com3')
    if not opened:
        print('Failed to connect Eilik.')
        exit(-1)

    while True:
        # user_input = console_input()
        status = EilikCom.read_status()
        if status["head"] is True:
            logger.debug('ready to listen')
            user_input = get_asr_response()
        else:
            time.sleep(.05)
            continue

        start = time.time()

        chat_history: list[ChatMessageItem] = []

        logger.debug(f"用户输入问题 input: {user_input}")

        desire_list_1 = [si for i in range(1, 30) for si in desire.get(f"D{i}").items]
        desire_name_list_1 = [item.name for item in desire_list_1]

        religion_1 = extract_religion(user_input, desire_name_list_1, chat_history)
        desire_1 = religion_1.desire

        desire_list_2: list[DesireItem] = desire_1.fetch_subtree(
            depth=1, including_self=True
        )
        desire_name_list_2 = [item.name for item in desire_list_2]

        religion_2 = extract_religion(user_input, desire_name_list_2, chat_history)

        end = time.time()

        feeling = map_religion_feeling(religion_2)

        action_id = feeling2eilik_action(feeling)
        EilikCom.execute_action(action_id)

        logger.info(f"最终选择的信念 religion: {religion_2}")
        logger.debug(f"信念对应感受 feeling: {feeling}")
        logger.debug(f"消耗的时间 cost_time: {end - start}")

        logger.info("本轮分析结束 [ROUND_END]")
        logger.info("-----------------------")

import datetime
import json
import time
import typing
from typing import Tuple, TypedDict

from device.asr import get_asr_response
from device.eilik import EilikCom, get_default_serial_name
from dui.llm import ChatMessageItem, LLM_inference
from dui.types import Religion
from dui.types import emotion as name_lib
from dui.types.desire import DESIRE_PROPERTY, DesireItem
from dui.types.emotion import Feeling
from dui.types.religion_feeling import map_religion_feeling
from dui.utils.data import load_data, save_config
from dui.utils.log import get_logger

logger = get_logger("desc2feeling", console_level="DEBUG")

SYSTEM_PROMPT_ONE = """
你扮演一个担任自然语言表达动机提取的AI程序。\
我将输入一句自然语言与欲望列表。 \
其中，欲望列表的每一项是一个三元组，三元组每个值的含义依次为（欲望名称，积极感受，消极感受） \
你先从我提供的欲望列表中，筛选出所有欲望名称，再选择与该自然语言表达动机最匹配的一项欲望名称。 \
同时，你需要判断表达者在说这句自然语言时的情绪状态是积极还是消极。 \
你第一反应的欲望很可能不是最匹配的，因此你需要一步步思考。\
我希望你只在一个唯一的代码块内回复 json，而不是其他任何内容。\
不要写解释，除非我指示你这样做，否则不要自行追加新的输入。
输入格式分为两行，第一行是自然语言的句子，第二行是欲望列表。
输出格式为 json 格式的字典，含有的键为  \
`desire`（欲望名称，来自输入列表）、valence （极性，true 积极 false 消极）
"""

SYSTEM_PROMPT_TWO = """
你扮演我的好朋友，和我对话，并引导我的情绪向积极的方向改变。 \
我会输入一句自然语言、该自然语言对应的信念、我说这句自然语言时的感受、历史对话记录。 \
其中，感受包括两部分，第一部分是感受类型，第二部分是感受程度，程度的范围是[0,500]，值越大表明感受越强烈。 \
历史对话记录的每一行包含以"事件:"开头的历史输入事件和以"回复:"开头的你的历史回复。\

你先在历史对话记录中提取与该自然语言相关的信息。 \
再基于提取出的信息，针对自然语言、信念、感受给出最合理的对话回复。 \
其中，如果感受是积极的，你需要表示共鸣，并通过回复增加我的该感受； \
如果感受是消极的，你需要表示不同意我的观点，生成具有同理心的回复，以减少我的该感受。

我希望你只在一个唯一的代码块内回复 json，而不是其他任何内容。\
不要写解释，除非我指示你这样做，否则不要自行追加新的输入。
输入格式分为四部分，第一部分是自然语言，第二部分是信念，第三部分是感受，第四部分是历史对话记录。
输出格式为 json 格式的字典，含有的键为 reply（对话回复）
"""

QUESTION_TEMPLATE = """
自然语言：{}
欲望列表：{}
"""

QUESTION_TEMPLATE_TWO = """
自然语言：{}
信念：{}
感受：{}
历史对话记录：{}
"""


def extract_religion(
    total_input: str,
    system_prompt,
    optional_desires: list[typing.Any],
    chat_history: list[ChatMessageItem],
) -> Religion:
    question = QUESTION_TEMPLATE.format(total_input, optional_desires)
    logger.debug(f"欲望备选：{optional_desires}")
    answer = LLM_inference(
        question=question,
        system_prompt=system_prompt,
        chat_history=chat_history,
        model="gpt-4",
    )
    religion_data = {}
    try:
        religion_data = json.loads(answer)
        # 错误验证
        required_keys = ['desire', 'valence']
        missing_keys = [
            key for key in required_keys if key not in religion_data]
        if missing_keys:
            raise KeyError(f"{missing_keys} not found in religion_data")

        desire_name = religion_data["desire"]
        valence = religion_data["valence"]

        religion = Religion(desire_name=desire_name, valence=valence)
        logger.debug(f'信念选择：本次推理选择 "{ religion }" 作为信念')

    except KeyError as e:
        logger.error(f"Invalid religion_data: {e}")
        religion = Religion(desire_name=answer)
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


def extract_religion_already(
    user_input: str,
    dialogue_event: str,
    feel,
    system_prompt,
    religion: Religion,
    chat_history: list[ChatMessageItem],
) -> str:
    question = QUESTION_TEMPLATE_TWO.format(
        user_input,
        str(religion),
        feel,
        dialogue_event
    )
    answer = LLM_inference(
        question=question,
        system_prompt=system_prompt,
        chat_history=chat_history,
        model="gpt-4",
    )
    religion_data = {}
    try:
        religion_data = json.loads(answer)
        # 错误验证
        if 'reply' not in religion_data:
            raise KeyError("reply not found in religion_data")

        reply = religion_data["reply"]

    except KeyError as e:
        reply = None
        logger.error(f"Invalid religion_data: {e}")
    except json.decoder.JSONDecodeError as e:
        reply = None
        logger.warn("Failed to decode LLM inference answer")
        logger.warn(f"{e.msg}")
    except Exception as e:
        reply = None
        logger.fatal("Unexpected Exception !!!")
        logger.fatal(f"{e}")
    finally:
        if reply is None or religion._desire_id == 'UNDEFINED':
            reply = "主人遇到什么事了,能详细说说吗?"

        return reply


def console_input() -> str:
    user_input = input("请输入事件：(输入quit结束运行~)\n")
    if user_input == "quit":
        exit(0)
    return user_input


class FEELING2ACTION_DATA_ITEM(TypedDict):
    feeling: str
    range_start: int
    range_end: int
    desc: str
    action_id: int


FEELING2ACTION_DATA: list[FEELING2ACTION_DATA_ITEM] = load_data(
    "feeling2action")


ALL_EMOTION_NAMES = name_lib.EMOTION_NAMES + [name_lib.EMOTION_NAME_DEFAULT]
ALL_EMOTION_NAMES_CN = name_lib.EMOTION_NAMES_CN + \
    [name_lib.EMOTION_NAME_DEFAULT_CN]

translate_emotion_name: dict[str, str] = dict(
    zip(ALL_EMOTION_NAMES_CN, ALL_EMOTION_NAMES)
)

mapping_feeling_action: dict[str, list[FEELING2ACTION_DATA_ITEM]] = dict(
    [
        (
            feeling_name,
            [
                item
                for item in FEELING2ACTION_DATA
                if translate_emotion_name[item["feeling"]] == feeling_name
            ],
        )
        for feeling_name in ALL_EMOTION_NAMES
    ]
)


def map_religion2action(religion: Religion) -> FEELING2ACTION_DATA_ITEM:
    feeling = map_religion_feeling(religion)
    return map_feeling2action(feeling)


def map_feeling2action(feeling: Feeling) -> FEELING2ACTION_DATA_ITEM:
    feeling_item = feeling.get_max_feeling_item(50)
    name, value = feeling_item

    optional_list = mapping_feeling_action[name]

    for i in optional_list:
        if i["range_start"] <= value < i["range_end"]:
            return i

    logger.warn("reach end of feeling2eilik_action")
    return mapping_feeling_action["calm"][0]


def feeling2eilik_action(feeling: Feeling) -> int:
    return map_feeling2action(feeling)["action_id"]


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def store_data(
        religion: str,
        time: str,
        user_input: str,
        reply: str
):

    file_data = load_data('background_event') or {}
    if religion in file_data:
        file_data[religion].append({
            'time': time,
            'user_input': user_input,
            'reply': reply
        })
    else:
        file_data[religion] = []
        file_data[religion].append({
            'time': time,
            'user_input': user_input,
            'reply': reply
        })
    save_config('background_event', file_data)


if __name__ == "__main__":
    desire = DESIRE_PROPERTY
    # EilikPortName = "com3"
    eilik_serial_name = get_default_serial_name()

    opened = EilikCom.open(port=eilik_serial_name)
    if not opened:
        print("Failed to connect Eilik.")
        exit(-1)

    record_event: str = ""

    while True:
        # user_input = console_input()
        status = EilikCom.read_status()
        if status["head"] is True:
            logger.debug("ready to listen")
            EilikCom.execute_action(3039018111)
            user_input = get_asr_response()
        else:
            time.sleep(0.05)
            continue

        right_event: str = ""
        total_event: str = ""
        start = time.time()
        EilikCom.execute_action(3039018113)
        chat_history: list[ChatMessageItem] = []
        right_event += user_input + " "

        logger.debug(f"用户输入问题 input: {user_input}")

        desire_list_1 = [si for i in range(1, 30)
                         for si in desire.get(f"D{i}").items]
        religions_list_1: list[Tuple[DesireItem, Religion, Religion]] = [
            (
                i,
                Religion(desire_item=i, valence=True),
                Religion(desire_item=i, valence=False),
            )
            for i in desire_list_1
        ]
        feelings_list_1: list[
            Tuple[DesireItem, FEELING2ACTION_DATA_ITEM, FEELING2ACTION_DATA_ITEM]
        ] = [
            (i, map_religion2action(p), map_religion2action(n))
            for (i, p, n) in religions_list_1
        ]

        desire_name_list_1 = [
            (i.name, p["desc"], n["desc"]) for (i, p, n) in feelings_list_1
        ]

        religion_1 = extract_religion(
            user_input,
            SYSTEM_PROMPT_ONE,
            desire_name_list_1,
            chat_history
        )

        background_data = load_data('background_event')
        if str(religion_1) in background_data:
            for item in background_data[str(religion_1)][-5:]:
                total_event += "事件:" + item['user_input'] + " "
                total_event += "回复:" + item['reply'] + "\n"
        if record_event:
            total_event += record_event
        total_event += user_input
        logger.debug(f"背景事件为:{total_event}")

        feeling = map_religion_feeling(religion_1)
        feeling_name, feeling_value = feeling.get_max_feeling_item()
        feel = {"感受类型": feeling_name, "感受值": feeling_value}
        logger.debug(f"感受是{feeling_name},感受值为{feeling_value}")

        religion_reply_2 = extract_religion_already(
            user_input,
            total_event,
            feel,
            SYSTEM_PROMPT_TWO,
            religion_1,
            []
        )

        right_event += "回复:" + religion_reply_2 + "\n"
        record_event += right_event
        store_data(str(religion_1), get_current_time(),
                   user_input, religion_reply_2)

        # desire_1 = religion_1.desire

        # desire_list_2: list[DesireItem] = desire_1.fetch_subtree(
        #     depth=1, including_self=True
        # )
        # desire_name_list_2 = [item.name for item in desire_list_2]

        # religion_2 = extract_religion(user_input, desire_name_list_2, chat_history)

        end = time.time()

        action_id = feeling2eilik_action(feeling)
        EilikCom.execute_action(action_id)

        logger.info(f"最终选择的信念 religion: {religion_1}")
        logger.debug(f"信念对应感受 feeling: {feeling}")
        logger.info(f"Eilik的回复是: {religion_reply_2}")
        logger.info(f"action: {action_id}")
        logger.debug(f"消耗的时间 cost_time: {end - start}")

        logger.info("本轮分析结束 [ROUND_END]")
        logger.info("-----------------------")

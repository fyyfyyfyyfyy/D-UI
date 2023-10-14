import os
import typing

import openai  # type: ignore

from dui.utils.log import get_logger

logger = get_logger("llm.connection")

openai.api_key = os.getenv("OPENAI_API_KEY")


def has_envvar(name: str):
    env_var = os.getenv(name)
    if env_var is None or len(env_var) <= 0:
        return False
    return True


if not has_envvar("https_proxy"):
    openai.api_base = "https://openkey.cloud/v1"  # 换成代理，一定要加v1

logger.info(f"using {openai.api_base} as api_base")


# define connection


class ChatMessageItem(typing.TypedDict):
    content: str
    role: str


def _get_message_item(content: str, role: str = "user") -> ChatMessageItem:
    return {"role": role, "content": content}


def GPT_completion(
    question,
    system_prompt: str = "",
    chat_history: list[ChatMessageItem] = [],
    model="gpt-3.5-turbo",
) -> str:
    messages_property = [_get_message_item(system_prompt, "system")]

    messages = messages_property if len(system_prompt) > 0 else []

    for i, chi in enumerate(chat_history):
        messages.append(chi)
        if "role" not in chi or "content" not in chi:
            logger.warn(f"invalid message item of chat_history[{i}]: {chi}")
        if "role" in chi and chi["role"] == "system":
            logger.warn('role "system" should not be used twice or more.')

    messages.append(_get_message_item(question))
    logger.debug(f"question对应的信息: {messages[-1]}")
    chat_history.append(messages[-1])

    logger.debug('----------- Start GPT Completion -----------')
    logger.debug(f"model = {model}, messages as following:")
    for m in messages:
        logger.debug(f"{m['role']}: {m['content']}")
    # logger.info(messages)
    completion = openai.ChatCompletion.create(
        model=model, messages=messages  # gpt-3.5-turbo, gpt-4 ...
    )

    answer = completion.choices[0].message
    answer_role: str = answer.role
    answer_content: str = answer.content

    logger.debug("completion output:")
    logger.debug(f"{answer_content}")
    logger.debug('----------- End GPT Completion -----------')

    chat_history.append(_get_message_item(answer_content, answer_role))
    return answer_content


def dumb_LLM_inference(*args, **kwargs) -> str:
    logger.warn("dumb_LLM_inference was called with following args:")
    logger.warn(f"args = {args}, kwargs = {kwargs}")
    return ""


def LLM_inference(
    question,
    system_prompt: str = "",
    chat_history: list[ChatMessageItem] = [],
    model="gpt-3.5-turbo",
    fake_LLM_func: typing.Callable = dumb_LLM_inference,
):
    if has_envvar("OPENAI_API_KEY"):
        return GPT_completion(
            question=question,
            chat_history=chat_history,
            model=model,
            system_prompt=system_prompt,
        )
    else:
        logger.warn("WARNING: fake LLM function is called.")
        return fake_LLM_func()

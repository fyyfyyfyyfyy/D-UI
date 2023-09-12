from datetime import datetime

from dui.llm import LLM_inference, event_to_prompt
from dui.types import Desire, Emotion, Event, History, Person, Religion
from dui.utils.log import get_logger

logger = get_logger(__name__, console_level='DEBUG')


if __name__ == '__main__':
    logger.info('welcome to D-UI !')

    desire = Desire()
    desire[2] = 85
    desire[3] = 75
    desire[4] = 60
    desire[6] = 40
    desire[7] = 40
    desire[9] = 30
    desire[18] = 70
    desire[21] = 60
    desire[22] = 60
    desire[23] = 60
    desire[27] = 80

    emotion = Emotion(item_values=[30])

    history = History.open("example/example_out_clean.json")
    logger.debug(f'History has {len(history)} items.')

    person = Person(desire, emotion, history=history)

    logger.debug(f'current desire is {person.desire}')

    location = "四川北路666号"
    environment = "和好朋友去了川菜馆"
    time = datetime.now()
    event = Event(location=location, environment=environment, time=time)

    religions = [Religion(desire_name="食物", valence=v) for v in [True, False]]

    prompt = event_to_prompt(event, person=person, religions=religions)

    logger.debug("PROMPT:")
    logger.info(prompt)

    answer = LLM_inference(question=prompt, history=person.history)

    logger.debug("ANSWER:")
    logger.info(answer)

    # 交互
    while (True):
        logger.debug('============================')
        iscontinue = input("请输入quit结束运行，输入start继续运行~\n")
        if (iscontinue == "quit"):
            break
        location = input("请输入地址:\n")
        environment = input("请输入发生的事件:\n")
        time = datetime.now()
        event = Event(location=location, environment=environment, time=time)

        # religion_str = ['吃辣让人舒适', '吃辣让人难受', '学习让人快乐', '学习让人难受']
        # religions = [Religion(rs, desire_name="食物") for rs in religion_str]
        # logger.debug("desire:" + str(religions[1].get_related_strength(desire)))

        prompt = event_to_prompt(
            event=event, person=person, religions=None)

        logger.debug("PROMPT:")
        logger.info(prompt)

        answer = LLM_inference(question=prompt, history=person.history)
        person.history_push(event)

        logger.debug("ANSWER:")
        logger.info(answer)

        # logger.debug("person.history:\n" + str(person.history))

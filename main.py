from datetime import datetime

from dui.llm import LLM_inference, event_to_prompt
from dui.types import Desire, Emotion, Event, Person, Religion

if __name__ == '__main__':
    print('welcome to D-UI !')

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

    person = Person(desire, emotion)

    location = "四川北路666号"
    environment = "和好朋友去了川菜馆"
    time = datetime.now()
    event = Event(location=location, environment=environment, time=time)

    religion_str = ['吃辣让人舒适', '吃辣让人难受', '学习让人快乐', '学习让人难受']
    religions = [Religion(rs) for rs in religion_str]

    prompt = event_to_prompt(event, person=person, religions=religions)

    print('prompt:', prompt)

    answer = LLM_inference(question=prompt)

    print('answer:', answer)
    # 交互
    while (True):
        iscontinue = input("请输入quit结束运行，输入start继续运行~\n")
        if (iscontinue == "quit"):
            break
        location = input("请输入地址:\n")
        environment = input("请输入发生的事件:\n")
        time = datetime.now()
        event = Event(location=location, environment=environment, time=time)
        person.history_push(event)
        religion_str = ['吃辣让人舒适', '吃辣让人难受', '学习让人快乐', '学习让人难受']
        religions = [Religion(rs) for rs in religion_str]
        print("desire:", religions[1].get_related_strength(desire))

        prompt = event_to_prompt(
            person.history[-1], person=person, religions=religions)

        print('prompt:', prompt)

        answer = LLM_inference(question=prompt)

        print('answer:', answer)

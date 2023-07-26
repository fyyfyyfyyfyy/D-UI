from datetime import datetime

from dui.llm import GPT_completion, event_to_prompt
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

    print(person)

    location = "四川北路666号"
    environment = "和好朋友去了川菜馆"
    time = datetime.now()
    event = Event(location=location, environment=environment, time=time)

    religion_str = ['吃辣让人舒适', '吃辣让人难受', '学习让人快乐', '学习让人难受']
    religions = [Religion(rs) for rs in religion_str]

    prompt = event_to_prompt(event, person=person, religions=religions)

    print('prompt:', prompt)

    answer = GPT_completion(question=prompt)

    print('answer:', answer)

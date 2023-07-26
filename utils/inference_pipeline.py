from invoke_GPT3 import GPT  # type: ignore


def get_event(background, emotions, desire, belief_list):
    event = '事件和场景为%s,初始情绪为%s,初始欲望为%s,信念列表为%s.' \
            % (background, emotions, desire, belief_list)
    json_limit = '请推理信念以及情绪变化,输出仅给出JSON, JSON格式示例:' \
        '{"belief": "学习", "emotion_change": {"happiness": +5, "anger": 0,' \
        'surprise": 0, "disgust": 0, "sadness": 0}}'
    return event + json_limit


if __name__ == "__main__":
    back = '(我和好朋友,四川北路666号,川菜馆,8:00pm)'
    emo = '[30,0,0,0,0]'
    des = '[0,0,85,75,60,0,40,40,0,30,0,0,0,0,0,0,0,0,70,0,0,60,60,60,0,0,80,0,0]'
    belief = '[吃辣让人舒适、吃辣让人难受、学习让人快乐、学习让人难受]'
    eve = get_event(background=back, emotions=emo, desire=des, belief_list=belief)
    answer = GPT(user='user', question=eve,
                 model='gpt-3.5-turbo', prompt='./utils/prompt.txt')
    print(answer)

import os

import openai  # type: ignore

openai.api_key = os.getenv('OPENAI_API_KEY')


def has_envvar(name: str):
    env_var = os.getenv(name)
    if env_var is None or len(env_var) <= 0:
        return False
    return True


if not has_envvar('https_proxy'):
    openai.api_base = "https://openkey.cloud/v1"  # 换成代理，一定要加v1


SYSTEM_PROMPT = '''You play the role of a psychologist,\
and I will input a number of events, scenarios and my states \
for example, desires, emotions and so on,\
as well as a list of beliefs from which\
you will need to select the one I am most likely to have given that event.\
Desires will be entered as key-value pairs with values [0,100],\
and emotions will be five dimensional vectors\
with values from 0 to 100 for each dimension,\
the five dimensions being "happy", "sad", "hate", "amazed", and "angry".\
Please reason about my mood changes based on them\
and consider only the effect of the belief on mood,\
ignoring other factors.\
Only the effect of this belief on mood should be considered,\
other factors have not been taken into account.\
Next is a case where I enter a list of beliefs as\
['Eating spicy food makes me happy', 'Eating spicy food makes me sad', \
'Studying makes me happy', 'Studying makes me sad'],\
Regarding output, you need to output your chosen beliefs\
and emotional changes, \
as well as predict my response to this event.\
Response is the form of a sentence in Chinese\
and includes an opening statement, \
a response statement, and an end-of-sentence phrase.\
A sample output is shown below:\
``` \
{"religion": "学习让人快乐", "emotion_delta": {\
"happy": 5, "sad": 0, "hate": 0, "amazed": 0, "angry": 0}
"answer": “哇！我最喜欢吃川菜了！太好了！”} \
```\
Before each output you need to analyze the reasons for choosing beliefs \
and mood changes in 100 words.\
Next I start the first input.\
You must output the JSON format data of the example above.\
The output in JSON format is preceded by the symbol ```json\
and followed by the symbol ```
Below I will do the input.
'''


def GPT_completion(question, user='user',
                   model='gpt-3.5-turbo', system_prompt=SYSTEM_PROMPT) -> str:
    completion = openai.ChatCompletion.create(
        model=model,  # gpt-3.5-turbo, gpt-4 ...
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": user, "content": question}
        ]
    )
    return completion.choices[0].message.content


def LLM_inference(question, user='user',
                  model='gpt-4', system_prompt=SYSTEM_PROMPT):
    if has_envvar('OPENAI_API_KEY'):
        return GPT_completion(question=question, user=user,
                              model=model, system_prompt=system_prompt)


if __name__ == "__main__":
    question = "事件为：今天中午，朋友小明对我说：“我们一起去吃清淡的菜吧！”，初始情绪为(30,0,0,0,0)，\
                初始欲望为\
                [0,0,85,75,60,0,40,40,0,30,0,0,0,0,0,0,0,0,70,0,0,60,60,60,0,0,80,0,0]，\
                信念列表为[吃辣让人舒适、吃辣让人难受、学习让人快乐、学习让人难受]"
    answer = LLM_inference(question=question)
    print(answer)

import os

import openai  # type: ignore

openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT3(user, question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": user, "content": question}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    answer = GPT3(user='user', question='我今天很开心')
    print(answer)

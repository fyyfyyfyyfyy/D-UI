import os

import openai  # type: ignore


def has_proxy():
    proxy_addr = os.getenv('https_proxy')
    if proxy_addr is None or len(proxy_addr) <= 0:
        return False
    return True


openai.api_key = os.getenv('OPENAI_API_KEY')

if not has_proxy():
    openai.api_base = "https://openkey.cloud/v1"  # 换成代理，一定要加v1


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

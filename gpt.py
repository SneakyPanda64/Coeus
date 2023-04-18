import os

import openai


def ChatCompletion(messages, max_tokens, temperature):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages
    )
    return response.choices[0].message.content
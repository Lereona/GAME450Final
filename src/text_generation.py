#!/usr/bin/python
import openai
#PLACE THE CHAT GPT API KEY HERE
key = "PLACE API KEY HERE"

def connection(key):
    OPENAI_API_KEY = key
    openai.api_key = OPENAI_API_KEY

def ask_ai(messages): 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=1.0,
        messages = messages
    )
    return response["choices"][0]["message"]["content"]


def bot_provoke_message():
    connect = connection(key)
    prompt = [{"role": "user", "content": "give me a single quote, max 7 words, for a provocative message for 'I will win in rock paper scissors!'"}]
    response = ask_ai(prompt)

    return response

def player_provoke_message():
    connect = connection(key)
    prompt = [{"role": "user", "content": "give me a single quote, max 7 words, for a provocative message for 'I will not lose either!'"}]
    response = ask_ai(prompt)

    return response

def bot_take_damage_message():
    connect = connection(key)
    prompt = [{"role": "user", "content": "give me a single quote for a message from a loser for 'That hurts!'"}]
    response = ask_ai(prompt)
    return response

def player_take_damage_message():
    connect = connection(key)
    prompt = [{"role": "user", "content": "give me a single quote for a message for 'That hurts! But I will still win'"}]
    response = ask_ai(prompt)
    return response

def player_taunt_pool():
    count = 0
    messages = []
    while count <4:
        messages += [player_provoke_message()]
        count += 1
    return messages

def bot_taunt_pool():
    count = 0
    messages = []
    while count <4:
        messages += [bot_provoke_message()]
        count += 1
    return messages





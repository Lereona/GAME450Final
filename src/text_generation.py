
#!/usr/bin/python
import openai
key = ""

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
    prompt = [{"role": "user", "content": "give me a single quote for a provocative message for 'I will win in rock paper scissors!'"}]
    response = ask_ai(prompt)

    return response

def player_provoke_message():
    connect = connection(key)
    prompt = [{"role": "user", "content": "give me a single quote for a provocative message for 'I will not lose either!'"}]
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


print(bot_provoke_message())
print(player_provoke_message())
print(bot_take_damage_message())
print(player_take_damage_message())



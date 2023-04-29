import openai
import os
from collections import deque
import time
from datetime import datetime
import argparse

# Set your OpenAI API key as an environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt3_response(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message['content'].strip()

def append_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')
def load_topic(topic_file):
    if os.path.exists(topic_file):
        with open(topic_file, 'r') as f:
            return f.read().strip()
    return None

def save_topic(topic_file, topic):
    with open(topic_file, 'w') as f:
        f.write(topic)

def get_agent_input(last_message, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": last_message}]
    agent_prompt = {"role": "assistant", "content": "As an agent, provide a helpful suggestion based on the last message in the conversation. If you can't provide any assistance, respond with 'No suggestion'."}
    messages.append(agent_prompt)

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message['content'].strip()

def main(participant1, participant2, model):
    topic_file = "topic.txt"

    previous_topic = load_topic(topic_file)
    if previous_topic:
        topic = input(f"Press enter to load the previous topic: {previous_topic} or give me a new topic: ")
        if not topic:
            topic = previous_topic
    else:
        topic = input("Give me a topic to discuss: ")

    save_topic(topic_file, topic)
    topicFilename = topic.replace(" ","_")
    filename = f"{participant1}_{participant2}_{topicFilename}.txt"

    initial_message = f"Hello there, I am {participant2}, it’s nice to meet you. I want to talk to you about {topic}, what do you think?"
    print(f"{participant2}: {initial_message}")
    append_to_file(filename, f"{participant2}: {initial_message}")

    conversation_history = deque(maxlen=30)
    conversation_history.append({"role": "system", "content": "You are a very educated, outgoing person and engaging person. You provide structured helpful answers and provide followup questions when necessary. Your goal is to come up with as many helpful discussion topics as possible and to keep the converation going but showing insight, and opening new conversational avanues. "})
    conversation_history.append({"role": "user", "content": initial_message})

    mod_counter = 0

    while True:
        # Instance 1 (participant1) response
        part1_prompt = list(conversation_history.copy())
        part1_prompt.append({"role": "assistant", "content": f"{participant1}:"})
        part1_response = get_gpt3_response(part1_prompt, model)
        print(f"{participant1}: {part1_response}")
        append_to_file(filename, f"{participant1}: {part1_response}")
        conversation_history.append({"role": "user", "content": part1_response})
        time.sleep(3)
        
        # Instance 2 (participant2) response
        part2_prompt = list(conversation_history.copy())
        part2_prompt.append({"role": "assistant", "content": f"{participant2}:"})
        part2_response = get_gpt3_response(part2_prompt, model)
        print(f"{participant2}: {part2_response}")
        append_to_file(filename, f"{participant2}: {part2_response}")
        conversation_history.append({"role": "user", "content": part2_response})
        time.sleep(3)
        
        # Moderator input every 3 turns
        mod_counter += 1
        if mod_counter % 3 == 0:
            mod_prompt = list(conversation_history.copy())
            mod_prompt.append({"role": "assistant", "content": "As a moderator, provide some extra helpful information that adds to the discussion. For instance, it maybe poses a new question that hasn't been discussed yet. Also, if you think the conversation Is not going anywhere, reply only with [END]. Mod:"})
            mod_response = get_gpt3_response(mod_prompt, "gpt-3.5-turbo")
            print(f"#Moderator: {mod_response}")
            append_to_file(filename, f"#Moderator: {mod_response}")
            conversation_history.append({"role": "user", "content": mod_response})
            time.sleep(3)

# Agent input
        last_message = conversation_history[-1]['content']
        agent_suggestion = get_agent_input(last_message, model)
        if agent_suggestion != "No suggestion":
            print(f"#Agent: {agent_suggestion}")
            append_to_file(filename, f"#Agent: {agent_suggestion}")
     
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--participants", help="Participants in the conversation, separated by a colon (e.g. 'Dave:Cindy')", default="Bob:Alice")
    parser.add_argument("-m", "--model", help="Model to use for the conversation (e.g. 'gpt-3.5-turbo')", default="gpt-3.5-turbo")
    args = parser.parse_args()

    participant1, participant2 = args.participants.split(':')
    main(participant1, participant2, args.model)

import json
import os

import openai
from openai.types.chat import ChatCompletion

agent_prompt = {"messages": []}
with open(r"prompts/tools.json", "r") as f:
    tools = json.load(f)

with open(r"prompts/agent.txt", "r") as f:
    agent_prompt = f.read()
    agent_prompt = {"messages": [{"role": "system", "content": agent_prompt}]}


def ask_permission(message: str):
    return input(f"{message} (y/n): ").lower() == "y"


def stop_exec(response):
    if len(response) <= 2:
        return False
    recent = response["messages"][-1]
    return (
        "role" in recent
        and recent["role"] == "assistant"
        and "tool_calls" not in recent
    )


def resolve_tool(tool_name: str, tool_args: str):
    pass


def loop(user_input: str):
    client = openai.Client(
        base_url=os.getenv("LLM_API_BASE_URL"), api_key=os.getenv("LLM_API_KEY")
    )
    agent_prompt["messages"].append({"role": "user", "content": user_input})
    while not stop_exec(agent_prompt) and len(agent_prompt["messages"]) < 10:
        print(f"step: {len(agent_prompt['messages'])}")
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-4-vision-preview", messages=agent_prompt["messages"], tools=tools
        )
        agent_prompt["messages"].append(response.choices[0].message.model_dump())

        if response.choices[0].message.tool_calls:
            for tool in response.choices[0].message.tool_calls:
                tool_name = tool.name
                tool_args = tool.arguments
                tool_result = ""
                print(f"Tool called: {tool_name} with arguments {tool_args}")
                tool_result = resolve_tool(tool_name, tool_args)

                agent_prompt["messages"].append(
                    {"role": "tool", "name": tool_name, "content": tool_result}
                )

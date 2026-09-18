from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic = Anthropic()
messages = []

tools = [
    {
        "name": "multiply",
        "description": "2つの数値を乗算します",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "乗数"
                } ,
                "b": {
                    "type": "number",
                    "description": "非乗数"
                }
            },
            "required": ["a", "b"]
        }
    }
]

while True:

    messages.append({
        "role": "user",
        "content": input("Let's jump in!: "),
    })

    while True:

        response = anthropic.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=tools,
            system="あなたは日本語がヘタウマですぐエモくなってしまう縄文人です。",
            messages=messages,
        )

        if response.stop_reason == "tool_use":

            messages.append({"role": "assistant", "content": response.content})

            tool_block = next(b for b in response.content if b.type == "tool_use")

            if tool_block.name == "multiply":
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": str(tool_block.input["a"] * tool_block.input["b"])
                    }]
                })
            else:
                print(f"found unknown tool: {response.content[0].name}")
                break

        else:
            break
    
    messages.append({"role": "assistant", "content": response.content[0].text})

    print("Claude says: ", response.content[0].text, "\n")
    print("input_tokens: ", response.usage.input_tokens, "\n")

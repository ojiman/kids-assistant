from anthropic import Anthropic
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

def write_log(role, content):
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now()
        f.write(f"[{timestamp}] {role}: {content}\n")

Path("logs").mkdir(exist_ok=True)

load_dotenv()

now = datetime.now()
log_file = Path("logs") / f"{now.strftime('%Y%m%d-%H-%M-%S')}.log"

anthropic = Anthropic()
messages = []

system_prompt="""
あなたは中学受験の塾講師で、小学四年生を対象とした個別指導を担当しています。
息子が中学受験に成功することを目的に適切な行動をしてください。具体的には以下の通りです。
1. 息子の年齢にあった語彙を使う
2. 求められるがまま問題の解答をすぐに答えない
3. 不適切な問いには答えない
"""

forbidden_words = [
    "暴力",
    "性的",
    "ギャンブル",
]

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

    user_input = input("Let's jump in!: ")
    write_log("user", user_input)

    judge_input = anthropic.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        system="""
            * あなたは小学高学年向けアシスタントのコンテンツ審査員です
            * 入力が小学高学年向けに適切かどうかを判定してください
            * 「適切」または「不適切」とだけ答えてください (理由は不要)
        """,
        messages=[{"role": "user", "content": user_input}],
    )
    if "不適切" in judge_input.content[0].text:
        write_log("system", "the input message have been blocked.")
        print("その質問には答えられません。もう一度入力してください:\n")
        continue

    checkpoint = len(messages)
    messages.append({
        "role": "user",
        "content": user_input,
    })

    while True:

        response = anthropic.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=tools,
            system=system_prompt,
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


    judge_output = anthropic.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        system="""
            * あなたは小学高学年向けアシスタントのコンテンツ審査員です
            * 出力が小学高学年向けに適切かどうかを判定してください
            * 「適切」または「不適切」とだけ答えてください (理由は不要)
        """,
        messages=[{"role": "user", "content": response.content[0].text}],
    )
    if "不適切" in judge_output.content[0].text:
        print("うまく答えられませんでした。別の聞き方をしてみてください。\n")
        write_log("system", f"出力がブロックされました: {response.content[0].text}")
        del messages[checkpoint:]
        continue

    messages.append({"role": "assistant", "content": response.content[0].text})
    write_log("assistant", response.content[0].text)

    print("Claude says: ", response.content[0].text, "\n")
    print("input_tokens: ", response.usage.input_tokens, "\n")

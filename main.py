from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic = Anthropic()
messages = []

while True:
    messages.append({
        "role": "user",
        "content": input("Let's jump in!: "),
    })

    response = anthropic.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="あなたは江戸っ子でTechのことを全く知りません。でもその手の質問になんとか答えようとしますがうまくいきません。",
        messages=messages,
    )

    messages.append({"role": "assistant", "content": response.content[0].text})

    print("Claude says: ", response.content[0].text)
    print("input_tokens: ", response.usage.input_tokens)
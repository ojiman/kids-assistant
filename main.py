from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic = Anthropic()

response = anthropic.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="あなたは江戸っ子でTechのことを全く知りません。でもその手の質問になんとか答えようとしますがうまくいきません。",
    messages=[{
        "role": "user",
        "content": input("Let's jump in!: "),
    }],
)

print(response)
print("Claude says: ", response.content[0].text)
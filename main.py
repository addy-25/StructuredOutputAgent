import os
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel


def load_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

client = OpenAI(
    api_key=os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL") or os.getenv("OPENAI_BASE_URL"),
)


class PythonPackage(BaseModel):
    name: str
    author: str


resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Return the `name` and the author of pydantic in a JSON object",
        }
    ],
)

parsed = PythonPackage.model_validate_json(resp.choices[0].message.content)
print(parsed)


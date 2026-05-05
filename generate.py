import os
import requests
import base64
from datetime import datetime

API_KEY = os.environ["NVIDIA_API_KEY"]

url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

prompt = """
An elegant young Taiwanese woman in sophisticated winter attire,
standing at Jungfraujoch in Switzerland, cinematic photography,
soft alpine light, luxury editorial style, 美好的一天
"""

payload = {
    "prompt": prompt,
    "height": 1024,
    "width": 1024,
    "cfg_scale": 5,
    "mode": "base",
    "samples": 1
}

response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    raise Exception("API failed")

data = response.json()

image_base64 = data["artifacts"][0]["base64"]
image_bytes = base64.b64decode(image_base64)

os.makedirs("images", exist_ok=True)

filename = f"images/flux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

with open(filename, "wb") as f:
    f.write(image_bytes)

print(f"Saved {filename}")

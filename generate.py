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
An elegant young Taiwanese woman in flowing Mediterranean-inspired attire, standing on a dramatic cliff overlooking the vast Aegean Sea in Greece during golden late afternoon light. She has a calm yet liberated expression with a soft smile and eyes gently facing the ocean horizon, conveying freedom, serenity, and timeless beauty. Cinematic composition, 85mm lens, shallow depth of field, subject in sharp focus, expansive sea softly glowing behind her. The background reveals towering seaside cliffs, endless deep-blue Aegean waters shimmering under sunlight, distant white villages perched along the coastline, and rugged Mediterranean rock formations shaped by sea wind and time. Warm sunlight blends with cool ocean reflections, creating luminous highlights and a clean, airy atmosphere filled with transparent sea air. A strong yet graceful sea breeze moves her flowing linen dress and hair naturally, creating elegant motion and a profound sense of openness. Elegant Chinese calligraphy reading "美好的一天" appears subtly and artistically integrated into the composition. Color palette: Aegean blue, sunlit white, pale gold, stone beige, Mediterranean sky tones. Greek island cinematic atmosphere, mythic coastal freedom, ethereal Mediterranean light, poetic travel photography, luxury lifestyle editorial, museum-quality composition.
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

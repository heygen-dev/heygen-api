"""The same client drives every hosted model listed in heygen_api.MODELS."""
from heygen_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"image_url": "https://example.com/input.png", "audio_url": "https://example.com/input.png"}, model="veed/fabric-1.0")
print(output)

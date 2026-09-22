# HeyGen API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/heygen/avatar-4?utm_source=github&utm_medium=ugc&utm_campaign=heygen-dev&utm_content=readme-badge&utm_term=tier-c)

HeyGen is an AI video platform best known for talking avatars: it turns a photo or a recorded likeness into a presenter that speaks a script in a chosen voice or lip-syncs to supplied audio. Avatar 4 is HeyGen's photo-driven model, which animates a single still image, including face, head and upper-body motion, from text or audio. This repository is a small Python client for the HeyGen API as hosted on Synexa, so you can generate avatar videos from a script with one `pip install` and an API token.

You get a blocking `run()` that takes a photo and a script or audio file and returns the video URL, a non-blocking create-and-poll path for batches, and webhook delivery for services that would rather be called back. The client has a single runtime dependency and no model weights. It is aimed at developers building personalised outreach, training and onboarding video, product explainers or localised presenter content who want HeyGen-class avatars as an HTTP call.

> **Try it now:** [https://synexa.ai/explore/heygen/avatar-4](https://synexa.ai/explore/heygen/avatar-4?utm_source=github&utm_medium=ugc&utm_campaign=heygen-dev&utm_content=readme-top&utm_term=tier-c) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About HeyGen](#about-heygen)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **The weights are not published.** Avatar 4 is a proprietary hosted model; there is no checkpoint to run locally, so an API endpoint is the only programmatic route, and this client wraps the Synexa one.
- **No GPU, TTS or lip-sync stack to assemble.** A self-built equivalent means a portrait animation model, a text-to-speech model and a lip-sync model chained on a datacenter GPU. The hosted endpoint runs all of it and you pay per video.
- **No cold start on your side.** The model is resident on the endpoint; a single request and a thousand personalised videos see the same latency profile, with nothing to warm up.
- **Predictable cost.** `heygen/avatar-4` is billed at $0.10 per run and the alternative `veed/fabric-1.0` at $0.08 per run, so the cost of a campaign is known before you submit it.

## Installation

```bash
pip install git+https://github.com/heygen-dev/heygen-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=heygen-dev&utm_content=readme-apikey&utm_term=tier-c)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import heygen_api

output = heygen_api.run({
    "image_url": "https://example.com/input.png"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from heygen_api import Client

client = Client(api_key="sk-...")
output = client.run({"image_url": "https://example.com/input.png"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`heygen/avatar-4`](https://synexa.ai/explore/heygen/avatar-4?utm_source=github&utm_medium=ugc&utm_campaign=heygen-dev&utm_content=readme-models&utm_term=tier-c) | image-to-video | Avatar 4 turns a photo into a talking avatar that speaks your text or lip-syncs to an audio file. | $0.1 |
| [`veed/fabric-1.0`](https://synexa.ai/explore/veed/fabric-1.0?utm_source=github&utm_medium=ugc&utm_campaign=heygen-dev&utm_content=readme-models&utm_term=tier-c) | image-to-video | Fabric 1.0 turns a photo plus an audio track into a talking-head video. | $0.08 |

The default model is **`heygen/avatar-4`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `heygen/avatar-4`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `image_url` | file | yes | — | — | Photo to animate (.jpg/.png/.webp). It must contain a clear face |
| `prompt` | string | no | `Hi - thanks for stopping by. Let me show…` | — | The text the avatar will speak |
| `voice` | string | no | — | — | Name of the voice to use for the avatar |
| `audio_url` | file | no | — | — | Optional speech for the avatar to lip-sync to (.mp3/.wav/.flac/.m4a/.ogg). When set, it overrides prompt and voice |
| `talking_style` | string | no | `stable` | stable, expressive | Talking style - 'stable' for minimal movement, 'expressive' for more animation |
| `expression` | string | no | — | — | Facial expression for the avatar to hold, e.g. friendly, serious, excited |
| `resolution` | string | no | `720p` | 360p, 480p, 540p, 720p, 1080p | Video resolution preset. Options: 360p, 480p, 540p, 720p, 1080p |
| `aspect_ratio` | string | no | `16:9` | 16:9, 9:16, 4:5, 5:4, 1:1, auto | Aspect ratio of the output video. Supported values: '16:9', '9:16', '4:5', '5:4', '1:1', and 'auto'. 'auto' preserves the source aspect ratio when HeyGen can read it, falling back to '16:9' otherwise. |
| `caption` | boolean | no | `False` | — | Whether to add captions to the video |

### `veed/fabric-1.0`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `image_url` | file | yes | — | — | Portrait to animate (.jpg/.png/.webp). One clear, forward-facing face works best |
| `audio_url` | file | yes | — | — | Speech for the portrait to lip-sync to (.mp3/.wav/.flac/.m4a/.ogg) |
| `resolution` | string | no | `720p` | 720p, 480p | Output resolution of the talking-head video |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from heygen_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About HeyGen

HeyGen ([heygen.com](https://www.heygen.com)) is an AI video platform focused on avatar-driven video. Its product line includes studio avatars recorded from real presenters, instant avatars created from a short webcam capture, photo avatars, video translation that re-voices and lip-syncs existing footage into other languages, and interactive avatars that respond in real time. It is used mainly for marketing, sales outreach, learning content and localisation, where the same script must be produced in many variants without a camera crew.

Avatar 4 (marketed as Avatar IV) is HeyGen's photo-to-video avatar model. From a single image with a clear face it generates a video in which the subject speaks, with lip movement, facial expression and natural head and upper-body motion driven by the audio. The hosted endpoint accepts either a `prompt` (the text to speak) plus a `voice` name, or an `audio_url` that the avatar lip-syncs to and which overrides text and voice. Further controls are `talking_style` (`stable` for minimal movement or `expressive` for more animation), an `expression` such as friendly or serious, `resolution` from 360p to 1080p, `aspect_ratio` including 16:9, 9:16, 4:5, 5:4, 1:1 and auto, and a `caption` switch. Output is a single video clip whose length follows the speech.

Typical uses are personalised sales videos generated per recipient, training modules narrated by a consistent presenter, multilingual versions of the same explainer, and social clips from a brand mascot or illustrated character. Limits to plan for: the source must contain one clear face, the output is only as long as the audio, and stylised or heavily occluded faces animate less reliably than a frontal portrait.

The hosted endpoint used by this client is `heygen/avatar-4` on Synexa, which is HeyGen's own Avatar 4 model served through Synexa's API. The client also exposes `veed/fabric-1.0`, a talking-head model from VEED that takes a portrait and an audio track; it is a different model, included as a lower-cost option when you already have the speech recorded. HeyGen's full platform, including studio avatars, video translation and interactive avatars, remains at [heygen.com](https://www.heygen.com).

**Official project:** https://www.heygen.com

## Use cases

- **Personalised sales outreach** — loop over a lead list, set `prompt` to a script with the recipient's name and company, and generate one video per lead through the poll path.
- **Training and onboarding modules** — use one presenter photo and a `stable` talking style so every lesson has the same calm delivery.
- **Multilingual explainers** — generate the same video in several languages by swapping `prompt` and `voice`, or pass translated `audio_url` files to control pronunciation.
- **Social clips from a mascot** — animate an illustrated character with `expressive` style and 9:16 output for short-form platforms.
- **Lip-sync to a recorded voiceover** — supply `audio_url` so a professionally recorded track drives the avatar instead of synthetic speech.
- **Low-cost talking heads** — route audio-only jobs to `veed/fabric-1.0` at $0.08 per run when you do not need Avatar 4's expression and style controls.

## FAQ

**Is there a HeyGen API?**

Yes. HeyGen offers a developer API on its own platform, and Avatar 4 is also hosted on Synexa as `heygen/avatar-4`. This client talks to the Synexa endpoint, which takes a photo and either a script or an audio file and returns a talking-avatar video.

**How much does the HeyGen API cost through this client?**

The hosted `heygen/avatar-4` endpoint is billed at $0.10 per run. The alternative `veed/fabric-1.0` talking-head model is $0.08 per run. There is no subscription; you pay per completed video.

**Can I run HeyGen without a GPU?**

With this client, yes. Generation happens on Synexa's GPUs; your machine only needs Python and network access. HeyGen's models are not available for local use.

**Does this client work with HeyGen studio avatars or video translation?**

No. It covers the photo-to-video Avatar 4 endpoint and VEED Fabric 1.0 only. Studio avatars, instant avatars, video translation and interactive avatars are features of HeyGen's own platform.

**What input formats does it accept?**

`image_url` is required and accepts .jpg, .png and .webp with one clear face. Speech comes from `prompt` plus `voice`, or from `audio_url` (.mp3, .wav, .flac, .m4a, .ogg), which overrides prompt and voice when set. Optional fields are `talking_style`, `expression`, `resolution` (360p to 1080p), `aspect_ratio` and `caption`.

**Is this the official HeyGen SDK?**

No. This is an independent client that wraps the Synexa-hosted endpoint. HeyGen's official product, API and SDKs are at https://www.heygen.com.

## Related

- [HeyGen](https://www.heygen.com) — official platform and developer API
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose SDK this client builds on
- [heygen/avatar-4 on Synexa](https://synexa.ai/explore/heygen/avatar-4) — the hosted Avatar 4 endpoint
- [veed/fabric-1.0 on Synexa](https://synexa.ai/explore/veed/fabric-1.0) — audio-driven talking-head video from a portrait
- [xiaomi/mimo-tts on Synexa](https://synexa.ai/explore/xiaomi/mimo-tts) — text-to-speech for producing the audio track first

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of HeyGen. Model weights and trademarks belong to their respective owners.


_Last reviewed: 2026-09-22_

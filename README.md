# Seedream 6 API — Python Client and Image Generation Examples

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

Generate and edit images with ByteDance Seedream through [MuAPI](https://muapi.ai). This repository includes a reusable Python client, text-to-image and image-edit examples, and cURL requests. MuAPI uses an asynchronous submit-and-poll workflow: generation calls return a request ID, and a separate result request returns the finished image.

**Status:** the Seedream 6 integration is coming soon and is not yet live on MuAPI. The examples here use the live Seedream 5.5 routes, and the same client structure is intended to carry over once Seedream 6 endpoints are published. No Seedream 6 fields, pricing, or release dates are assumed.

## Related Projects

- [Seedream 6 API on MuAPI](https://muapi.ai/seedream-6)
- [Seedream 5.5 API](https://muapi.ai/seedream-5.5) — live text-to-image, edit, and layer decomposition models.
- [MuAPI API reference](https://muapi.ai/docs/api-reference)
- [MuAPI API keys](https://muapi.ai/access-keys)
- [GPT Image 3 API](https://github.com/Anil-matcha/GPT-Image-3-API) — related image generation and editing examples.
- [Awesome AI Image Models](https://github.com/Anil-matcha/awesome-ai-image-models) — compare image models and API providers.
- [Open Generative AI](https://github.com/Anil-matcha/Open-Generative-AI) — generative-media tools and workflows.

## Features

- Seedream 5.5 text-to-image with 8 aspect ratios and 1K, 1.5K, and 2K tiers.
- Seedream 5.5 image editing with up to 10 reference images.
- Transparent-background output and PNG or JPEG formats.
- A reusable Python client with request submission, task polling, and error handling.
- Copy-paste cURL examples for both API workflows.

## Installation

```bash
git clone https://github.com/Anil-matcha/Seedream-6-API.git
cd Seedream-6-API
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MUAPI_API_KEY="your_muapi_api_key"
```

The examples require Python 3.9+ and `requests`. You can also copy `.env.example` to `.env` and load it with your preferred environment-variable tool.

## Text-to-image

```bash
python -m examples.generate
```

```python
from seedream_api import SeedreamAPI

api = SeedreamAPI()  # Reads MUAPI_API_KEY from the environment
job = api.generate(
    prompt="A cozy street-side cafe in Lisbon at golden hour, photorealistic",
    aspect_ratio="16:9",
    resolution="2K",
)
result = api.wait_for_completion(job["request_id"])
print(result)
```

## Image editing

Pass up to 10 public source-image URLs and an instruction describing the edit. Omit `aspect_ratio` to match the first input image.

```bash
export MUAPI_INPUT_IMAGE_URL="https://example.com/scene.jpg"
python -m examples.edit
```

```python
from seedream_api import SeedreamAPI

api = SeedreamAPI()
job = api.edit(
    prompt="Change the scene to a rainy blue-hour evening, keep the subject and composition unchanged",
    images_list=["https://example.com/scene.jpg"],
    resolution="2K",
)
print(api.wait_for_completion(job["request_id"]))
```

For local files, first upload the image using MuAPI's [file upload endpoint](https://muapi.ai/docs/api-reference), then pass the returned URL in `images_list`.

## cURL

Text-to-image:

```bash
curl -X POST "https://api.muapi.ai/api/v1/seedream-5.5" \
  -H "x-api-key: ${MUAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cozy street-side cafe in Lisbon at golden hour, photorealistic",
    "aspect_ratio": "16:9",
    "resolution": "2K"
  }'
```

Image edit:

```bash
curl -X POST "https://api.muapi.ai/api/v1/seedream-5.5-edit" \
  -H "x-api-key: ${MUAPI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Change the scene to a rainy blue-hour evening, keep the subject unchanged",
    "images_list": ["https://example.com/scene.jpg"],
    "resolution": "2K"
  }'
```

Poll for the result with the returned `request_id`:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  -H "x-api-key: ${MUAPI_API_KEY}"
```

## API reference

Base URL: `https://api.muapi.ai/api/v1`

| Workflow | Method and route | Required fields |
| --- | --- | --- |
| Text-to-image | `POST /seedream-5.5` | `prompt` |
| Image edit | `POST /seedream-5.5-edit` | `prompt`, `images_list` |
| Poll for result | `GET /predictions/{request_id}/result` | Path parameter `request_id` |

Every request uses the `x-api-key` header.

| Field | Generation | Editing | Values and limits |
| --- | --- | --- | --- |
| `prompt` | Required | Required | Text prompt or edit instruction |
| `images_list` | — | Required | Array of 1–10 publicly accessible image URLs |
| `aspect_ratio` | Optional | Optional | `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `2:3`, `3:2`, `21:9`. Generation default `1:1`; editing matches the first input image when omitted. |
| `resolution` | Optional | Optional | `1K`, `1.5K`, `2K`; default `1K` |
| `output_format` | Optional | Optional | `png` or `jpeg`; default `png` |
| `background` | Optional | Optional | `auto`, `transparent`, `opaque`; default `auto`. `transparent` forces PNG. |

See the [Seedream 5.5 page](https://muapi.ai/seedream-5.5) for current route availability and pricing.

## Asynchronous workflow

1. Submit a generation or edit request with your MuAPI API key.
2. Store the `request_id` from the response.
3. Poll `/api/v1/predictions/{request_id}/result`, or call `wait_for_completion` in the Python client.
4. When status is `completed`, read the image URL from the result. If it is `failed`, inspect the returned error details.

## Errors and practical notes

- HTTP errors from rejected submission or polling requests are raised by `requests.raise_for_status()`.
- Input images must be reachable by MuAPI. Upload local images before submitting an edit job.
- Keep `MUAPI_API_KEY` in an environment variable or secret store; never commit credentials.
- Follow [muapi.ai/seedream-6](https://muapi.ai/seedream-6) for Seedream 6 availability updates.

## License

MIT. See [LICENSE](LICENSE).

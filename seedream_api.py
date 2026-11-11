"""Small Python client for Seedream image generation via MuAPI."""

import os
import time

import requests


class SeedreamAPI:
    """Submit Seedream generation/edit jobs and poll their results."""

    def __init__(self, api_key=None, base_url="https://api.muapi.ai/api/v1"):
        self.api_key = api_key or os.environ.get("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("Set MUAPI_API_KEY or pass api_key to SeedreamAPI")
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

    def _submit(self, route, payload):
        response = requests.post(
            f"{self.base_url}/{route}", headers=self.headers, json=payload, timeout=60
        )
        response.raise_for_status()
        return response.json()

    def generate(
        self,
        prompt,
        aspect_ratio="1:1",
        resolution="1K",
        output_format="png",
        background="auto",
    ):
        """Submit a Seedream 5.5 text-to-image job."""
        return self._submit(
            "seedream-5.5",
            {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "resolution": resolution,
                "output_format": output_format,
                "background": background,
            },
        )

    def edit(
        self,
        prompt,
        images_list,
        aspect_ratio=None,
        resolution="1K",
        output_format="png",
        background="auto",
    ):
        """Submit a Seedream 5.5 edit with up to ten reference image URLs."""
        if not images_list or len(images_list) > 10:
            raise ValueError("images_list must contain between 1 and 10 image URLs")
        payload = {
            "prompt": prompt,
            "images_list": images_list,
            "resolution": resolution,
            "output_format": output_format,
            "background": background,
        }
        if aspect_ratio:  # omit to match the first input image
            payload["aspect_ratio"] = aspect_ratio
        return self._submit("seedream-5.5-edit", payload)

    def get_result(self, request_id):
        response = requests.get(
            f"{self.base_url}/predictions/{request_id}/result",
            headers={"x-api-key": self.api_key},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id, timeout=900, poll_interval=2):
        """Poll until completion or failure; return the final response JSON."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.get_result(request_id)
            status = result.get("status")
            if status == "completed":
                return result
            if status == "failed":
                raise RuntimeError(result)
            time.sleep(poll_interval)
        raise TimeoutError(f"Generation {request_id} did not finish within {timeout}s")

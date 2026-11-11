"""Edit an image through MuAPI's Seedream edit endpoint."""

import os

from seedream_api import SeedreamAPI


def main():
    image_url = os.environ.get("MUAPI_INPUT_IMAGE_URL")
    if not image_url:
        raise SystemExit("Set MUAPI_INPUT_IMAGE_URL to a public image URL")
    api = SeedreamAPI()
    job = api.edit(
        prompt="Change the scene to a rainy blue-hour evening, keep the subject and composition unchanged",
        images_list=[image_url],
        resolution="1K",
    )
    request_id = job["request_id"]
    print(f"Submitted request: {request_id}")
    print(api.wait_for_completion(request_id))


if __name__ == "__main__":
    main()

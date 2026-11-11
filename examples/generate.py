"""Generate an image through MuAPI's Seedream endpoint."""

from seedream_api import SeedreamAPI


def main():
    api = SeedreamAPI()
    job = api.generate(
        prompt=(
            "A cozy street-side cafe in Lisbon at golden hour, warm natural light, "
            "blue azulejo tiles, photorealistic, shot on 35mm"
        ),
        aspect_ratio="16:9",
        resolution="1K",
    )
    request_id = job["request_id"]
    print(f"Submitted request: {request_id}")
    print(api.wait_for_completion(request_id))


if __name__ == "__main__":
    main()

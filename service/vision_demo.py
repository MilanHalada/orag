from pathlib import Path

from service.config import VISION_SUPPORTED_SUFFIXES
from service.lmstudio_client import create_client
from service.vision import describe_image_cached

MAX_IMAGES = 5

def main() -> None:
    client = create_client()


    print("Prechadzam obrazky: ")

    images = [
        path
        for path in Path("../sample_images").iterdir()
        if path.is_file() and path.suffix.lower() in VISION_SUPPORTED_SUFFIXES
    ]


    for index, image in enumerate(images, start=1):

        print(f"{index}. {image.name}" , end="\r")

        if index > MAX_IMAGES:
            break

        description = describe_image_cached(client, image)

        print("Vision popis:")
        print()
        print(description)


if __name__ == "__main__":
    main()
from io import BytesIO

from django.core.files import File
import PIL.Image


def resize_image(image: File, size: tuple[int, int]) -> File:
    new_image = BytesIO()

    with PIL.Image.open(image) as pillow_image:
        resized_image = pillow_image.resize(size, resample=1, reducing_gap=2)
        resized_image.save(
            new_image, format=pillow_image.format, optimize=True, quality=70
        )

    return File(new_image, name=image.name)

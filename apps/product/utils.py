from io import BytesIO

from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile
import PIL.Image



def make_thumbnail(image: ImageFieldFile, size: tuple[int, int]) -> ContentFile:
    thumbnail_io = BytesIO()

    with PIL.Image.open(image) as pil_img:  # type: ignore
        resized_img = pil_img.resize(size, PIL.Image.Resampling.LANCZOS, reducing_gap=2)
        resized_img.save(thumbnail_io, pil_img.format, optimize=True, quality=85)

    return ContentFile(thumbnail_io.getvalue(), name=image.name)
